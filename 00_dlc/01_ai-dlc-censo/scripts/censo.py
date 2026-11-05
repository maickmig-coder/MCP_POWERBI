#!/usr/bin/env python3
"""CENSO BI — ritual AI-DLC v2.1. Genera, valida y registra el censo de un tablero Power BI en PBIP.

La única salida es un Markdown. El script hace todo el trabajo mecánico (inventarios, IDs, posiciones, bindings,
dependencias, clasificación de uso, conciliación); la IA solo completa los marcadores [IA: ...].

Comandos (todos de solo lectura sobre el PBIP):
  borrador    Lee el PBIP y escribe "<BI> - censo.md" con todo lo mecánico resuelto.
  pendientes  Lista los marcadores [IA: ...] que faltan, con su línea.
  validar     Revisa el Markdown y lo concilia contra el PBIP.
  comparar    Compara el borrador con el censo vigente: traslada validaciones y escribe el bloque de cambios.
  iniciar-validacion  Prepara un borrador de tipo Validación (mismo PBIP) para registrar respuestas del dueño.
  registrar   Valida y, si no hay errores, cierra la ejecución: historial, registro de cambios y archivo del censo anterior.
  guia-validacion  Ficha de cada punto pendiente, en orden, para presentarlo al dueño uno por uno (R59).
  vigencia    Dice si el censo corresponde a la última versión del PBIP y si es apto para el DLC de modificación.
  inventario  (diagnóstico) Vuelca a JSON lo que el script lee del PBIP.

Ejemplos:
  python scripts/censo.py borrador --pbip "C:/.../01_versiones/00_original/GC - Flotillas" --salida "C:/.../02_censo/GC - Flotillas" \
      --version 00_original --tipo Inicial --correo-ejecutor a@b.co --correo-dueno-tablero c@d.co
  python scripts/censo.py pendientes --markdown "C:/.../GC - Flotillas - censo.md"
  python scripts/censo.py validar   --pbip "C:/.../GC - Flotillas" --markdown "C:/.../GC - Flotillas - censo.md"
  python scripts/censo.py registrar --pbip "C:/.../GC - Flotillas" --markdown "C:/.../GC - Flotillas - censo.md" --alcance "..."

Requiere solo Python 3.9+ (sin paquetes externos).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from censo_analisis import TARJETAS, TIPO_LEGIBLE, analyze  # noqa: E402
from censo_lectura import elide_long_literals, read_pbip  # noqa: E402
import censo_versiones as cv  # noqa: E402

RITUAL = "2.3.3"
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass

CAT = {
    "estado_uso": {"En uso", "Uso técnico", "Sin uso interno identificado", "Uso desconocido", "Referencia rota"},
    "estado_censo": {"Completado y validado", "Completado pendiente de validación", "Revisión incompleta", "Interrumpido", "Fallido"},
    "tipo_censo": {"Inicial", "Actualización", "Validación"},
    "tipo_hallazgo": {"Hallazgo", "Riesgo", "Vacío", "Observación"},
    "prioridad": {"Alta", "Media", "Baja"},
    "estado_punto": {"Pendiente de validación", "Confirmado por el dueño", "Descartado por el dueño"},
    "certeza": {"Encontrado", "Inferido", "Desconocido"},
}
SECCIONES = ["Control obligatorio previo", "Identificación", "Objetivo y alcance", "Fuentes de datos y conexiones", "Transformaciones",
             "Modelo de datos", "Columnas", "Medidas", "Páginas", "Visuales", "KPIs", "Filtros, segmentaciones e interacciones",
             "Bookmarks, botones y navegación", "Recursos, tema y presentación", "Reglas de negocio", "Dependencias",
             "Hallazgos, vacíos y puntos de revisión", "Limitaciones y control para DLC posteriores", "Validación final"]
CLASES = ["V", "F", "D", "M", "PQ", "BK", "SQL", "SEC"]
OBLIGATORIAS = ["V", "F", "D", "M", "PQ", "BK"]
VERBOS = re.compile(r"\b(cambiar|eliminar|reemplazar|corregir|desactivar|retirar|depurar|borrar|quitar|usar\s+\S+\s+en\s+lugar\s+de)\b", re.I)
TRUNC = re.compile(r"\b[0-9a-f][0-9a-f-]{5,}(?:…|\.\.\.)")
APROX = re.compile(r"(≈|~\s*\d|\baprox\.?\s*\d|\baproximadamente\s+\d)", re.I)
EMAIL = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
CID = re.compile(r"^\d{8}T\d{6}-[a-z0-9-]+$")
FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2})?([+-]\d{2}:\d{2}|Z)$")
IA = re.compile(r"\[IA:[^\]]*\]")


# =============================================================================================
# Markdown
# =============================================================================================
def cell(v):
    if v is None or v == "" or v == []:
        return "—"
    if isinstance(v, bool):
        return "Sí" if v else "No"
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return str(v).replace("|", "\\|").replace("\n", " ").strip() or "—"


def tabla(headers, rows, num=()):
    if not rows:
        return "_Sin registros._\n"
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---:" if h in num else "---" for h in headers) + "|"]
    out += ["| " + " | ".join(cell(x) for x in r) + " |" for r in rows]
    return "\n".join(out) + "\n"


def code(lang, text):
    fence = "````" if "```" in text else "```"
    return f"{fence}{lang}\n{text.rstrip()}\n{fence}\n"


def ref_txt(t, c):
    return f"Expresión «{c}»" if t is None else f"{t}[{c}]"


# =============================================================================================
# Borrador
# =============================================================================================
def render(inv: dict, a: dict, args, census_id: str, fecha: str) -> str:
    bi = Path(inv["raiz"]).name
    R, M = inv.get("report_dir", "—"), inv.get("model_dir", "—")
    tablas = inv.get("tablas", [])
    reales = [t for t in tablas if not t["auto"]]
    autos = [t for t in tablas if t["auto"]]
    vis = inv.get("visuales", [])
    pages = inv.get("paginas", [])
    pname = {p["page_id"]: p["pagina"] for p in pages}
    vi = a["visual_info"]
    a["pname"] = pname
    L = []
    w = L.append

    # ---------------------------------------------------------------- 0 y encabezado
    w("# 0. Control obligatorio previo\n")
    w(f"- **Correo de quien realiza el CENSO:** {args.correo_ejecutor}")
    w(f"- **Correo del dueño/responsable del tablero:** {args.correo_dueno_tablero}\n")
    w("Ambos correos se registraron antes de leer el PBIP (R02).\n\n---\n")
    w(f"# Censo BI — {bi}\n")
    w("> Estado: [IA: valor de CAT-07 al cerrar el censo]\n>")
    w(f"> census_id: {census_id}\n>")
    w(f"> Fecha y hora de ejecución: {fecha}\n>")
    w(f"> Versión analizada: {args.version}\n>")
    w(f"> Huella del PBIP: {args.huella} ({args.huella_n} archivos)\n>")
    w(f"> Tipo de CENSO: {args.tipo}\n>")
    w(f"> Versión del ritual: {RITUAL}\n")
    w("Convenciones de todo el documento: los IDs son nativos y completos (CAT-15); `—` = no aplica o no disponible; "
      "las rutas de evidencia se indican una vez por tabla, relativas a la carpeta del BI. Cada dato aparece en un solo lugar; "
      "las demás secciones lo citan por su ID.\n\n---\n")

    # ---------------------------------------------------------------- 1
    w("# 1. Identificación\n")
    props = inv.get("propiedades", {})
    w(tabla(["Campo", "Valor"], [
        ["census_id", census_id], ["census_id del censo anterior", args.census_anterior or "No aplica"],
        ["Nombre BI", bi], ["Archivo .pbip", ", ".join(inv.get("pbip", [])) or "No encontrado"],
        ["Área", "[IA: área de negocio, con certeza Encontrado/Inferido]"],
        ["Tecnología", f"Power BI PBIP — reporte PBIR, modelo TMDL, compatibilityLevel {props.get('compatibilityLevel', '—')}"],
        ["Repositorio", "No identificado en el PBIP"], ["Ambiente", "No identificado en el PBIP"],
        ["Archivos de salida", f"`{bi} - censo.md`, `historial-censos.md`"],
    ]))

    # ---------------------------------------------------------------- 2
    w("# 2. Objetivo y alcance\n")
    w("## 2.1 Objetivo del BI\n\n[IA: 2–4 frases: qué entrega el tablero, a quién y con qué grano de dato. Indicar certeza. No afirmar lo que un vacío de la sección 16 declara desconocido: si no se sabe qué es un campo, no se le pone adjetivo. Ejemplo: no «valor facturado (ver V01)», sino «valor (`Tabla[Valor]`, definición pendiente: V01)».]\n")
    w("## 2.2 Pregunta central\n\n[IA: una frase que responda ¿qué información entrega este BI y para qué se usa?]\n")
    w("## 2.3 Alcance del censo\n")
    w("Lectura de solo lectura de todo el PBIP con `scripts/censo.py borrador`: modelo TMDL (tablas, columnas, medidas, relaciones, "
      "jerarquías, roles, particiones M), reporte PBIR (páginas, visuales, bindings, filtros, interacciones, bookmarks, botones, "
      "recursos y tema). No incluye datos (filas), el servicio Power BI, la fuente de datos ni consumidores externos.\n")
    w("## 2.4 Fuentes inspeccionadas\n")
    w(tabla(["Elemento", "Ruta", "Objetos leídos"], [
        ["Tablas TMDL", f"{M}/definition/tables/", len(tablas)], ["Relaciones", f"{M}/definition/relationships.tmdl", len(inv.get("relaciones", []))],
        ["Roles", f"{M}/definition/roles/", len(inv.get("roles", []))], ["Páginas", f"{R}/definition/pages/", len(pages)],
        ["Visuales", f"{R}/definition/pages/*/visuals/", len(vis)], ["Bookmarks", f"{R}/definition/bookmarks/", len(inv.get("bookmarks", []))],
        ["Recursos", f"{R}/StaticResources/", len(inv.get("recursos", []))],
    ], num=("Objetos leídos",)))
    if inv.get("advertencias"):
        w("Advertencias de lectura: " + "; ".join(inv["advertencias"]) + "\n")

    # ---------------------------------------------------------------- 3
    w("# 3. Fuentes de datos y conexiones\n")
    w(f"Evidencia: particiones en `{M}/definition/tables/<Tabla>.tmdl`.\n")
    rows = []
    for i, q in enumerate(a["consultas"], 1):
        s0 = q["pasos"][0] if q["pasos"] else {}
        nav = [n for st in q["pasos"] for n in st.get("navegacion", [])]
        func = s0.get("funcion") or "—"
        arg = re.match(r"\s*[\w.#]+\s*\(\s*(\"[^\"]{0,60}\")", s0.get("codigo", "")) if s0 else None
        conn = f"{func}({arg.group(1)})" if arg and func != "—" else func
        if s0.get("op") == "Tabla embebida":
            conn = "Tabla embebida (base64)"
        rows.append([f"F{i:02d}", q["tabla"], q["particion"], q["modo"], s0.get("op", "—"), conn, " / ".join(nav) or "—"])
    for t in reales:
        for p in t["particiones"]:
            if p["tipo"].startswith("calculated"):
                rows.append([f"F{len(rows) + 1:02d}", t["tabla"], p["nombre"], p["modo"], "Tabla calculada DAX", "—", "—"])
    w(tabla(["fuente_id", "Tabla del modelo", "Partición", "Modo", "Tipo", "Conector", "Navegación"], rows))
    w("El código M completo de cada consulta está en la sección 4.\n")
    if autos:
        w(f"Las {len(autos)} tablas de fecha automáticas son tablas calculadas que genera Power BI (ver 6.2); no son fuentes.\n")
    params = inv.get("parametros", [])
    w("**Parámetros M:** " + ("; ".join(f"`{p['nombre']}` = `{cell(p['expr'])[:120]}`" for p in params) if params else "No aplica (sin `expressions.tmdl`).") + "\n")
    w("Credenciales: el PBIP no contiene credenciales; no se registran (R06). Frecuencia de actualización y propietario: ver sección 16.\n")

    # ---------------------------------------------------------------- 4
    w("# 4. Transformaciones (Power Query/M)\n")
    w("El código M completo de cada consulta está aquí una sola vez. Los renombres y tipos finales por columna están en la Matriz A "
      "(columnas «Nombre en origen» y «Tipo»), no se repiten en la tabla de pasos.\n")
    for i, q in enumerate(a["consultas"], 1):
        w(f"## 4.{i} {q['tabla']} (partición `{q['particion']}`, {len(q['pasos'])} pasos)\n")
        w(f"Evidencia: `{q['ruta']}`.\n")
        w(code("m", elide_long_literals(q["codigo"], q["ruta"])))
        prow = []
        for st in q["pasos"]:
            if st["renombres"]:
                af = f"{len(st['renombres'])} renombre(s)"
            elif st["tipos"]:
                af = f"{len(st['tipos'])} cambio(s) de tipo: " + ", ".join(c for c, _ in st["tipos"]) if len(st["tipos"]) <= 3 else \
                    f"{len(st['tipos'])} cambios de tipo"
            elif st["eliminadas"]:
                af = "Elimina: " + ", ".join(st["eliminadas"])
            else:
                af = ", ".join(st["afecta"]) or "—"
            prow.append([st["idx"], st["paso"], st["op"], af])
        w(tabla(["#", "Paso", "Operación", "Columnas afectadas"], prow, num=("#",)))

    # ---------------------------------------------------------------- 5
    w("# 5. Modelo de datos\n")
    w("## 5.1 Tablas\n")
    w(f"Evidencia: `{M}/definition/tables/<Tabla>.tmdl`.\n")
    rows = []
    for t in reales:
        rol = "Calculada DAX" if any(p["tipo"].startswith("calculated") for p in t["particiones"]) else \
            ("Solo medidas" if not t["columnas"] and t["medidas"] else "Importada (M)" if t["particiones"] else "—")
        rows.append([t["table_id"], t["tabla"], rol, "Oculta" if t["oculta"] else "Visible", len(t["columnas"]), len(t["medidas"]),
                     ", ".join(f"{p['nombre']} ({p['modo']})" for p in t["particiones"]) or "—"])
    w(tabla(["table_id", "Tabla", "Origen", "Visibilidad", "Columnas", "Medidas", "Particiones (modo)"], rows, num=("Columnas", "Medidas")))
    if autos:
        w(f"Además, {len(autos)} tablas de fecha automáticas (inventario en 6.2).\n")
    w("[IA: indicar en una lista corta el rol (hechos, dimensión, auxiliar) y la granularidad de cada tabla de la 5.1.]\n")
    w("## 5.2 Relaciones\n")
    w(f"Evidencia: `{M}/definition/relationships.tmdl`.\n")
    w(tabla(["relationship_id", "Desde", "Hacia", "Cardinalidad", "Filtro", "Activa", "joinOnDateBehavior"],
            [[r["relationship_id"], ref_txt(r["tabla_desde"], r["columna_desde"]), ref_txt(r["tabla_hacia"], r["columna_hacia"]),
              f"{r['card_desde']}:{r['card_hacia']}", r["filtro"], r["activa"], r["join_fecha"]] for r in inv.get("relaciones", [])]))
    w("## 5.3 Jerarquías y ordenamiento\n")
    hrows = [[h["hierarchy_id"], t["tabla"], h["nombre"], " > ".join(f"{lv} ({c})" for lv, c in h["niveles"])] for t in reales for h in t["jerarquias"]]
    w(tabla(["hierarchy_id", "Tabla", "Jerarquía", "Niveles (columna)"], hrows))
    srt = [[ref_txt(t["tabla"], c["nombre"]), c["sort_by"]] for t in reales for c in t["columnas"] if c.get("sort_by")]
    w("Ordenamiento (`sortByColumn`): " + ("; ".join(f"{x} por {y}" for x, y in srt) if srt else "ninguno.") +
      (f" Las {len(autos)} tablas automáticas tienen su jerarquía de fechas propia." if autos else "") + "\n")
    w("## 5.4 Propiedades del modelo\n")
    w(tabla(["Propiedad", "Valor"], [[k, v] for k, v in props.items()]))
    w("## 5.5 Seguridad\n")
    rr = [[r["rol"], r["permiso"], tbl, expr or "Sin expresión"] for r in inv.get("roles", []) for tbl, expr in (r["filtros"] or [("—", "Sin reglas RLS")])]
    w(tabla(["Rol", "Permiso", "Tabla", "Expresión RLS"], rr) if rr else "No aplica: el modelo no tiene roles.\n")

    # ---------------------------------------------------------------- 6
    w("# 6. Columnas\n")
    has_sql = bool(a["native_sql"])
    has_sec = a["has_roles"]
    cls = OBLIGATORIAS + (["SQL"] if has_sql else []) + (["SEC"] if has_sec else [])
    w("Clases de dependencia (CAT-03): V visuales · F filtros y segmentaciones · D DAX · M relaciones, jerarquías y ordenamiento · "
      "PQ pasos de Power Query · BK bookmarks" + (" · SQL consulta nativa" if has_sql else "") + (" · SEC seguridad" if has_sec else "") + ".")
    w("Valor de cada celda (CAT-04): número = referencias encontradas · `0` = no encontrada en el alcance revisado · `NA` = no aplica · "
      "`NV` = no verificable · `P` = pendiente." + ("" if has_sql else " SQL: no aplica (no hay consulta nativa en el PBIP).") +
      ("" if has_sec else " SEC: no aplica (sin roles).") + " El detalle de cada referencia está en su sección de origen "
      "(V → 9, F → 11, D → 6.1 expresiones y 7, M → 5, BK → 12).\n")
    w("## 6.1 Matriz A — columnas por tabla\n")
    for t in reales:
        w(f"### {t['tabla']} ({len(t['columnas'])} columnas)\n")
        w(f"Evidencia: `{t['ruta']}`.\n")
        rows = []
        for c in t["columnas"]:
            r = a["col_rows"][(t["tabla"], c["nombre"])]
            clase = "Calculada DAX" if c["calculada"] else "Origen"
            rows.append([c["column_id"], c["nombre"], r["origen"] if not c["calculada"] else "—", c["tipo_dato"] or "—", clase,
                         "Oculta" if c["oculta"] else "Visible"] + [r["clases"][k] for k in cls] + [r["estado"], r["nota"]])
        w(tabla(["column_id", "Columna", "Nombre en origen", "Tipo", "Clase", "Visibilidad"] + cls + ["Estado de uso", "Nota"], rows))
        calc = [c for c in t["columnas"] if c["calculada"]]
        if calc:
            w(f"Expresiones de columnas calculadas de {t['tabla']}:\n")
            w(code("dax", "\n\n".join(f"-- {c['nombre']}\n{c['expr']}" for c in calc)))
    if autos:
        w("## 6.2 Tablas de fecha automáticas\n")
        w("Las genera Power BI por la inteligencia de tiempo automática; tienen la misma estructura. Se listan sus IDs completos por columna.\n")
        rel_by_tab = {r["tabla_hacia"]: ref_txt(r["tabla_desde"], r["columna_desde"]) for r in inv.get("relaciones", [])}
        rows = []
        for t in autos:
            estados = Counter(a["col_rows"][(t["tabla"], c["nombre"])]["estado"] for c in t["columnas"])
            rows.append([t["table_id"], t["tabla"], rel_by_tab.get(t["tabla"], "Plantilla (sin relación)"), len(t["columnas"]),
                         "; ".join(f"{c['nombre']}={c['column_id']}" for c in t["columnas"]),
                         ", ".join(f"{k} {v}" for k, v in estados.items())])
        w(tabla(["table_id", "Tabla", "Origen (relación)", "Columnas", "column_id por columna", "Estado de uso"], rows, num=("Columnas",)))

    # ---------------------------------------------------------------- 7
    w("# 7. Medidas\n")
    w(f"Evidencia: `{M}/definition/tables/<Tabla>.tmdl`. Las expresiones completas están en el bloque de código al final de la sección.\n")
    rows = []
    allm = [(t, m) for t in tablas for m in t["medidas"]]
    for t, m in allm:
        r = a["meas_rows"][(t["tabla"], m["nombre"])]
        rows.append([m["measure_id"], m["nombre"], t["tabla"], m["formato"] or "—", ", ".join(r["usa"]) or "—", r["V"], r["F"], r["BK"], r["D"],
                     r["estado"], r["nota"]])
    w(tabla(["measure_id", "Medida", "Tabla", "Formato", "Usa", "V", "F", "BK", "D", "Estado de uso", "Nota"], rows))
    if allm:
        w(code("dax", "\n\n".join(f"-- {t['tabla']}[{m['nombre']}]\n{m['expr'] or '(sin expresión)'}" for t, m in allm)))

    # ---------------------------------------------------------------- utilidades de nombres
    def vn(vid, pid=None):
        """«visual_id · nombre» para que el visual se identifique sin abrir el PBIP."""
        v = a["by_vid"].get(vid)
        if v is None:
            return f"{vid} · no existe en el PBIP"
        return f"{vid} · {vi[(v['page_id'], vid)]['nombre']}"

    def pn(pid):
        if pid in (None, "—"):
            return "—"
        return f"{pid} · {pname[pid]}" if pid in pname else f"{pid} · no existe en el PBIP"

    bks = inv.get("bookmarks", [])
    bname = {b["bookmark_id"]: b["nombre"] for b in bks}

    def bn(bid):
        if not bid:
            return "—"
        return f"{bid} · {bname[bid]}" if bid in bname else f"{bid} · no existe en el PBIP"

    # ---------------------------------------------------------------- 8
    w("# 8. Páginas\n")
    w(f"Evidencia: `{R}/definition/pages/<page_id>/page.json`.\n")
    w(tabla(["page_id", "Página", "Orden", "Visibilidad", "Tamaño", "Ajuste", "Fondo", "Tipo", "Visuales"],
            [[p["page_id"], p["pagina"], p["orden"], p["visibilidad"], f"{p['ancho']}×{p['alto']}", p["display"], p["fondo"], p["tipo"],
              p["total_visuales"]] for p in sorted(pages, key=lambda x: x["orden"] or 99)], num=("Orden", "Visuales")))
    if a["phantom_pages"]:
        w("**Páginas referenciadas que no existen:**\n")
        w(tabla(["page_id", "Bookmarks que la usan", "Botones que navegan a ella"],
                [[k, "; ".join(bn(b) for b in v["bookmarks"]) or "—", "; ".join(vn(x) for x in v["botones"]) or "—"]
                 for k, v in a["phantom_pages"].items()]))

    # ---------------------------------------------------------------- 9
    w("# 9. Visuales\n")
    w(f"Evidencia: `{R}/definition/pages/<page_id>/visuals/<visual_id>/visual.json`. Posición y tamaño en píxeles enteros del lienzo.\n")
    w("Por cada página hay dos tablas: la primera dice **qué es y dónde está** cada visual (una fila por visual); la segunda, "
      "**qué datos usa** (una fila por campo). Clases: «Con binding válido» = muestra datos y todos sus campos existen; «Decorativo» = "
      "imagen, forma o texto sin datos; «Botón/acción»; «Referencia rota» = algún campo de datos apunta a una entidad que no existe, "
      "por lo que el visual no puede dibujarse. Un «Formato huérfano» es una regla de formato (colores por categoría, formato "
      "condicional) que apunta a una entidad inexistente: no impide que el visual funcione y no lo convierte en referencia rota.\n")
    resumen = []
    for i, p in enumerate(sorted(pages, key=lambda x: x["orden"] or 99), 1):
        pv = [v for v in vis if v["page_id"] == p["page_id"]]
        w(f"## 9.{i} {p['pagina']} (`{p['page_id']}`) — {len(pv)} visuales\n")
        w(tabla(["visual_id", "Nombre", "Tipo", "Oculto", "x", "y", "Ancho", "Alto", "z", "Grupo", "Clase", "Formato huérfano", "Estado de uso"],
                [[v["visual_id"], vi[(p["page_id"], v["visual_id"])]["nombre"], v["tipo"], v["oculto"], v["x"], v["y"], v["ancho"],
                  v["alto"], v["z"], v["grupo"], vi[(p["page_id"], v["visual_id"])]["clase"],
                  vi[(p["page_id"], v["visual_id"])]["formato_huerfano"], vi[(p["page_id"], v["visual_id"])]["estado"]]
                 for v in pv], num=("x", "y", "Ancho", "Alto", "z")))
        brow = []
        for v in pv:
            nm = vi[(p["page_id"], v["visual_id"])]["nombre"]
            for b in v["bindings"]:
                brow.append([v["visual_id"], nm, b["rol"], ref_txt(b["tabla"], b["campo"]), b["agregacion"], b.get("estado_ref", "—")])
            for kind, ent, prop, agg, est in v.get("otros_ref", []):
                brow.append([v["visual_id"], nm, "Formato/propiedad", ref_txt(ent, prop), agg or "—", est])
        w(f"Bindings de {p['pagina']} ({len(brow)}):\n")
        w(tabla(["visual_id", "Visual", "Rol", "Campo", "Agregación", "Referencia"], brow))
        c = Counter(vi[(p["page_id"], v["visual_id"])]["clase"] for v in pv)
        fh = sum(1 for v in pv if vi[(p["page_id"], v["visual_id"])]["formato_huerfano"])
        resumen.append([p["page_id"], p["pagina"], p["total_visuales"], len(pv), c["Con binding válido"], c["Decorativo"], c["Botón/acción"],
                        c["Referencia rota"], sum(c.values()), fh])
    w(f"## 9.{len(pages) + 1} Conciliación por página\n")
    tot = [sum(r[k] for r in resumen) for k in range(2, 10)]
    w(tabla(["page_id", "Página", "visual.json en PBIP", "Fichas", "Con binding válido", "Decorativos", "Botones/acciones", "Con referencia rota",
             "Suma", "Con formato huérfano (informativo)"], resumen + [["Total", "—"] + tot],
            num=("visual.json en PBIP", "Fichas", "Con binding válido", "Decorativos", "Botones/acciones", "Con referencia rota", "Suma",
                 "Con formato huérfano (informativo)")))
    w("La columna «Suma» debe ser igual a «visual.json en PBIP». «Con formato huérfano» no suma: esos visuales ya están contados en su clase.\n")

    # ---------------------------------------------------------------- 10
    w("# 10. KPIs\n")
    w("Se listan los visuales de tipo tarjeta o indicador con lo que calculan realmente.\n")
    w("[IA: completar la columna «Interpretación funcional». Si el título no coincide con lo calculado, registrarlo en la sección 16 "
      "(o ajustar la fila H-A que ya lo cubre).]\n")
    rows = []
    for v in vis:
        if v["tipo"] in TARJETAS:
            calc = "; ".join((f"{b['agregacion']}({ref_txt(b['tabla'], b['campo'])})" if b["agregacion"] not in ("—",) else f"[{b['campo']}]")
                             for b in v["bindings"]) or "—"
            rows.append([pname.get(v["page_id"]), v["visual_id"], vi[(v["page_id"], v["visual_id"])]["nombre"], calc, v["oculto"], "—"])
    w(tabla(["Página", "visual_id", "Título", "Calcula", "Oculto", "Interpretación funcional"], rows))

    # ---------------------------------------------------------------- 11
    w("# 11. Filtros, segmentaciones e interacciones\n")
    flt = inv.get("filtros", [])
    w(f"## 11.1 Filtros ({len(flt)})\n")
    w("Evidencia: `filterConfig` de `report.json` (Informe), `page.json` (Página) y `visual.json` (Visual).\n")
    w(tabla(["filter_id", "Ámbito", "Página", "Visual", "Campo", "Tipo", "Condición", "Oculto", "Bloqueado", "Invertido"],
            [[f["filter_id"], f["ambito"], pn(f["page_id"]), vn(f["visual_id"]) if f["visual_id"] not in ("—", None) else "—",
              ref_txt(f["tabla"], f["campo"]), f["tipo"], f["condicion"], f["oculto"], f["bloqueado"], f["invertido"]] for f in flt]))
    sl = [v for v in vis if (v["tipo"] or "").lower().startswith("slicer")]
    w(f"## 11.2 Segmentaciones ({len(sl)})\n")
    w(tabla(["visual_id", "Segmentación", "Página", "Modo", "Selección única", "Grupo de sincronización"],
            [[v["visual_id"], vi[(v["page_id"], v["visual_id"])]["nombre"], pn(v["page_id"]), v["slicer_modo"] or "—",
              v["slicer_unico"] if v["slicer_unico"] is not None else "—", v["sync"] or "—"] for v in sl]))
    it = inv.get("interacciones", [])
    w(f"## 11.3 Interacciones ({len(it)})\n")
    w("Evidencia: `visualInteractions` de cada `page.json`.\n")
    w(tabla(["Página", "Visual origen", "Visual destino", "Tipo"], [[pn(x["page_id"]), vn(x["origen"]), vn(x["destino"]), x["tipo"]] for x in it]))

    # ---------------------------------------------------------------- 12
    w("# 12. Bookmarks, botones y navegación\n")
    w(f"Evidencia: `{R}/definition/bookmarks/<bookmark_id>.bookmark.json`.\n")
    w(f"## 12.1 Bookmarks ({len(bks)})\n")
    opts = Counter(b["opciones"] for b in bks)
    comun = opts.most_common(1)[0][0] if opts else "—"
    w(f"Opciones comunes a la mayoría de los bookmarks: `{comun}`. Solo se indican en la tabla las que difieren.\n")
    w("«Targets» son los visuales a los que se aplica el bookmark (`targetVisualNames`). Un target puede **existir** en el PBIP y aun así "
      "**no funcionar** (referencia rota de datos). El estado del bookmark considera ambas cosas.\n")
    w(tabla(["bookmark_id", "Nombre", "Página", "Opciones distintas", "Targets: total / existen / funcionan", "Invocado por", "Estado de uso", "Motivo"],
            [[b["bookmark_id"], b["nombre"], pn(b["seccion"]), b["opciones"] if b["opciones"] != comun else "—",
              f"{len(b['targets_detalle'])} / {sum(d['existe'] for d in b['targets_detalle'])} / {sum(d['funciona'] for d in b['targets_detalle'])}",
              "; ".join(vn(x) for x in b["invocado_por"]) or "—", b["estado"], b["motivo"]] for b in bks]))
    w("## 12.2 Detalle de cada bookmark\n")
    w("Una fila por bookmark y efecto. «Se aplica» = lo que realmente pasa al activar el bookmark. «Guardado sin efecto» = estados que "
      "Power BI guardó al crear el bookmark (foto de toda la página) pero que no se aplican porque el bookmark solo actúa sobre sus "
      "targets (`applyOnlyToTargetVisuals`). Cada visual se lista como `visual_id · nombre · funciona/roto`.\n")

    def vfun(vid):
        v = a["by_vid"].get(vid)
        if v is None:
            return f"{vid} · no existe en el PBIP"
        info = vi[(v["page_id"], vid)]
        return f"{vid} · {info['nombre']} · {'roto' if info['rota'] else 'funciona'}"

    drow = []
    for b in bks:
        tgt = b["targets_detalle"]
        if tgt:
            for efecto in ("Muestra", "Oculta", "Sin estado guardado"):
                ids = [d["id"] for d in tgt if d["existe"] and d["efecto"] == efecto]
                if ids:
                    drow.append([b["bookmark_id"], b["nombre"], pn(b["seccion"]), f"Se aplica: {efecto.lower()}", len(ids), "; ".join(vfun(x) for x in ids)])
            miss = [d["id"] for d in tgt if not d["existe"]]
            if miss:
                drow.append([b["bookmark_id"], b["nombre"], pn(b["seccion"]), "Target inexistente", len(miss), "; ".join(f"{x} · no existe en el PBIP" for x in miss)])
        else:
            for efecto in ("Muestra", "Oculta"):
                ids = [x for x, st in b["estados_aplicados"].items() if st == efecto]
                if ids:
                    drow.append([b["bookmark_id"], b["nombre"], pn(b["seccion"]), f"Se aplica (toda la página): {efecto.lower()}", len(ids),
                                 "; ".join(vfun(x) for x in ids)])
        if b["estados_sin_efecto"]:
            drow.append([b["bookmark_id"], b["nombre"], pn(b["seccion"]), "Guardado sin efecto", len(b["estados_sin_efecto"]),
                         "Detalle por visual en 12.3"])
    w(tabla(["bookmark_id", "Bookmark", "Página", "Efecto", "Cantidad", "Visuales (visual_id · nombre · estado)"], drow, num=("Cantidad",)))
    w("## 12.3 Estados guardados sin efecto\n")
    w("Matriz por página: una fila por visual y una columna por bookmark. `O` = guardado oculto, `V` = guardado visible, `·` = sin estado "
      "guardado en ese bookmark. Son estados que Power BI guardó en la foto de la página pero que no se aplican porque el bookmark "
      "solo actúa sobre sus targets (12.2). Se mapean para que un cambio futuro sobre el bookmark (por ejemplo, quitar "
      "`applyOnlyToTargetVisuals`) conozca su efecto.\n")
    by_sec = defaultdict(list)
    for b in bks:
        if b["estados_sin_efecto"]:
            by_sec[b["seccion"]].append(b)
    if not by_sec:
        w("Ninguno.\n")
    for sec, bl in by_sec.items():
        vids = sorted({x for b in bl for x in b["estados_sin_efecto"]}, key=lambda x: (x not in a["by_vid"], vfun(x).split(" · ")[1] if x in a["by_vid"] else x))
        w(f"### {pn(sec)}\n")
        w("Columnas: " + "; ".join(f"**B{i}** = {bn(b['bookmark_id'])}" for i, b in enumerate(bl, 1)) + ".\n")
        mrows = []
        for x in vids:
            mrows.append([vfun(x)] + [("O" if b["estados_guardados"].get(x) == "Oculta" else "V") if x in b["estados_sin_efecto"] else "·"
                                      for b in bl])
        w(tabla(["Visual (visual_id · nombre · estado)"] + [f"B{i}" for i in range(1, len(bl) + 1)], mrows))
    w("## 12.4 Botones y acciones\n")
    btn = [(v, ac) for v, ac in ((v, ac) for v in vis for ac in v["acciones"]) if ac.get("type")]

    def destino(ac):
        d = ac.get("navigationSection") or ac.get("drillthroughSection")
        if d:
            return pn(d)
        return ac.get("webUrl") or "—"
    w(tabla(["Botón (visual_id · nombre)", "Página", "Acción", "Destino", "Bookmark asociado"],
            [[vn(v["visual_id"]), pn(v["page_id"]), ac.get("type"), destino(ac), bn(ac.get("bookmark"))] for v, ac in btn]))
    w("## 12.5 Tooltips y drillthrough\n")
    tt = [p for p in pages if p["tipo"] in ("Tooltip", "Drillthrough")]
    w(tabla(["page_id", "Página", "Tipo"], [[p["page_id"], p["pagina"], p["tipo"]] for p in tt]) if tt else "No encontrado: ninguna página es de tipo Tooltip o Drillthrough.\n")
    w("El efecto real al activar cada bookmark o botón no se ve en los archivos; se declara en 17.1.\n")

    # ---------------------------------------------------------------- 13
    w("# 13. Recursos, tema y presentación\n")
    w("Sección de estética: archivos gráficos, dónde está ubicado cada elemento visual de diseño (banners, logos, formas, textos) y el tema.\n")
    rec = inv.get("recursos", [])
    w(f"## 13.1 Archivos de recursos ({len(rec)})\n")
    w(f"Rutas relativas a la carpeta del BI (`{inv['raiz'].replace(chr(92), '/')}`).\n")
    w(tabla(["resource_id", "Tipo", "Ruta del archivo", "Peso (bytes)", "Tamaño original (px)", "Usos", "Estado de uso"],
            [[r["resource_id"], r.get("tipo") or "—", r.get("ruta"), r.get("peso"), f"{r['ancho']}×{r['alto']}" if r.get("ancho") else "—",
              len(r.get("usado_por", [])), r.get("estado")] for r in rec], num=("Peso (bytes)", "Usos")))
    w("## 13.2 Ubicación de los elementos de diseño por página\n")
    w("Incluye todo lo que está dentro de un banner (también tarjetas y segmentaciones, porque forman parte de su composición) y, fuera "
      "del banner, las imágenes, formas, textos y botones. Un banner es una forma que ocupa al menos el 80 % del ancho de la página; "
      "pertenecen a él los elementos que quedan dentro de su franja vertical. Tamaño colocado frente al original indica la escala de "
      "cada imagen.\n")
    rec_by = {r["resource_id"]: r for r in rec}
    for p in sorted(pages, key=lambda x: x["orden"] or 99):
        pv = [v for v in vis if v["page_id"] == p["page_id"]]
        W = p["ancho"] or 1280
        bands = sorted([v for v in pv if v["tipo"] in ("shape", "basicShape") and (v["ancho"] or 0) >= 0.8 * W and not v["oculto"]],
                       key=lambda v: v["y"] or 0)
        rows = []
        usados = set()
        for k, bnd in enumerate(bands, 1):
            y0, y1 = (bnd["y"] or 0), (bnd["y"] or 0) + (bnd["alto"] or 0)
            zona = "Banner superior" if k == 1 and y0 <= 0.1 * (p["alto"] or 720) else f"Banner {k}"
            dentro = [v for v in pv if (v["y"] or 0) >= y0 - 2 and (v["y"] or 0) + (v["alto"] or 0) <= y1 + 2 and not v["oculto"]]
            for v in sorted(dentro, key=lambda v: (v["y"] or 0, v["x"] or 0)):
                usados.add(v["visual_id"])
                rows.append(_fila_disenio(zona, v, bnd, vi, rec_by))
        for v in sorted(pv, key=lambda v: (v["y"] or 0, v["x"] or 0)):
            if v["visual_id"] not in usados and (v["tipo"] in ("image", "shape", "basicShape", "textbox", "actionButton") or v.get("recurso")):
                rows.append(_fila_disenio("Cuerpo de la página", v, None, vi, rec_by))
        w(f"### {p['pagina']} (`{p['page_id']}`)\n")
        w(tabla(["Zona", "visual_id", "Elemento", "Rol en el diseño", "x", "y", "Ancho", "Alto", "z", "Oculto", "Imagen (archivo · original → colocado)"],
                rows, num=("x", "y", "Ancho", "Alto", "z")))
    w("## 13.3 Tema\n")
    td = inv.get("tema_detalle", {})
    w(tabla(["Tema", "Nombre", "Archivo", "dataColors", "Fondo", "Primer plano", "Fuentes"],
            [[k, x.get("nombre"), x.get("archivo"), x.get("dataColors"), x.get("background"), x.get("foreground"), x.get("fuentes")]
             for k, x in td.items()]) if td else "No se encontró tema en `report.json`.\n")
    w("## 13.4 Metadatos del proyecto\n")
    md_ = inv.get("metadatos", {})
    w(tabla(["Elemento", "Valor"], [["Archivo .pbip", ", ".join(inv.get("pbip", []))], ["Modelo referenciado por el reporte", md_.get("modelo_referenciado")],
                                    ["Versión PBIR", md_.get("version_pbir")], ["logicalId del reporte", md_.get("report_logicalId")],
                                    ["logicalId del modelo", md_.get("model_logicalId")], ["Página activa al abrir", pn(md_.get("pagina_activa"))]]))

    # ---------------------------------------------------------------- 14
    w("# 14. Reglas de negocio\n")
    w("La implementación remite al objeto que la contiene; el código está en las secciones 4, 6.1 y 11. Los filtros sin condición "
      "guardada no son reglas (siguen inventariados en 11.1).\n")
    w("[IA: completar «Interpretación funcional», «Certeza» y «Validación del dueño» («No requerida» si es Encontrado; «Pendiente de validación» si es Inferido, hasta que el dueño responda, R55); agregar reglas que solo se deduzcan del conjunto. Una columna calculada se interpreta desde su expresión en 6.1 (no desde su nombre) y respetando su «Estado de uso»; su significado de negocio es «Inferido» (R51).]\n")
    rr, n = [], 0
    for q in a["consultas"]:
        for st in q["pasos"]:
            if st["op"] == "Filtro de filas":
                n += 1
                rr.append([f"RN{n:02d}", f"Filtro de carga en {q['tabla']}", f"Paso {st['idx']} «{st['paso']}» (4): {cell(st['codigo'])[:140]}", "—", "—"])
    for t in reales:
        for c in t["columnas"]:
            if c["calculada"]:
                n += 1
                rr.append([f"RN{n:02d}", f"Columna calculada {c['nombre']}", f"{ref_txt(t['tabla'], c['nombre'])} (6.1)", "—", "—"])
    for f in flt:
        if f["ambito"] in ("Página", "Informe") and f["condicion"] != "Sin condición guardada":
            n += 1
            rr.append([f"RN{n:02d}", f"Filtro de {f['ambito'].lower()} en {pname.get(f['page_id'], 'todo el informe')}",
                       f"{f['filter_id']}: {ref_txt(f['tabla'], f['campo'])} {f['condicion']} (11.1)", "—", "—"])
    rr = [r + ["—", "—"] for r in rr]
    w(tabla(["rule_id", "Regla", "Implementación (dónde)", "Interpretación funcional", "Certeza", "Validación del dueño", "Respuesta del dueño"], rr))

    # ---------------------------------------------------------------- 15
    w("# 15. Dependencias\n")
    top = sorted(((len(v), k) for k, v in a["consumers"].items() if k[0] == "measure"), reverse=True)[:3]
    aisl = [t["tabla"] for t in reales if not any(r["tabla_desde"] == t["tabla"] or r["tabla_hacia"] == t["tabla"] for r in inv.get("relaciones", []))]
    w("- Medidas más referenciadas por otras medidas: " + (", ".join(f"[{k[2]}] ({n})" for n, k in top) or "ninguna") + ".")
    w("- Tablas sin relaciones con otras tablas: " + (", ".join(aisl) or "ninguna") + ".\n")
    w("[IA: mapa de arquitectura en un bloque `text` de 5–12 líneas: Fuente → Consulta → Tabla → Columna/Medida → Visual → Página → KPI. "
      "No repetir conteos ni hallazgos: citar su ID de la sección 16.]\n")

    # ---------------------------------------------------------------- 16
    w("# 16. Hallazgos, vacíos y puntos de revisión\n")
    w("Tabla maestra única (R45): hallazgos, riesgos, observaciones y vacíos de información, una fila por asunto. Las filas `H-A*` y `V-A*` "
      "las genera el script; la IA revisa certeza, prioridad e impacto y agrega las de negocio (`H01`, `V01`…). No se repite un asunto "
      "que ya cubre otra fila: se ajusta esa fila. La columna «Punto de revisión» no usa verbos de cambio (R47).\n")
    w("[IA: revisar las filas H-A y V-A, ajustar prioridad/impacto y agregar hallazgos o vacíos de negocio que no estén cubiertos "
      "(por ejemplo, títulos que no coinciden con lo calculado en la sección 10 o definiciones de KPI sin confirmar).]\n")
    w(tabla(["ID", "Tipo", "Categoría", "Descripción concreta", "Página y objeto", "page_id", "visual_id / object_id (con nombre)", "bookmark_id / estado",
             "Evidencia exacta", "Certeza", "Objetos afectados y dependencias", "Impacto", "Prioridad", "Punto de revisión", "Validación requerida", "Estado", "Respuesta del dueño"],
            [r + ["—"] for r in hallazgos(inv, a, pname, vn, bn) + vacios(args)]))

    # ---------------------------------------------------------------- 17
    w("# 17. Limitaciones y control para DLC posteriores\n")
    w("## 17.1 Limitaciones\n")
    lim = ["Censo estructural: no se ejecutó el modelo ni se vieron datos; un binding correcto no garantiza el valor mostrado.",
           "La fuente de datos (sección 3) no se consultó; el uso de columnas fuera del PBIP no es verificable.",
           "El efecto en ejecución de bookmarks y botones requiere validación visual en Power BI Desktop.",
           "Literales de más de 300 caracteres en M (por ejemplo, tablas embebidas en base64) se omiten en la sección 4; están en el TMDL. Del contenido de esas tablas (por ejemplo, un mapeo de homologación) solo se documenta su efecto en el modelo.",
           "El censo describe solo la versión analizada del PBIP; los cambios respecto a versiones anteriores están en «[BI] - cambios.md» (R52)."]
    w("\n".join(f"{i}. {x}" for i, x in enumerate(lim, 1)) + "\n")
    w("[IA: agregar solo limitaciones del proceso del censo (qué no se pudo revisar y por qué) o escribir «Sin limitaciones adicionales». Los problemas del tablero van en la sección 16, no aquí.]\n")
    w("## 17.2 Candidatas a depuración\n")
    w("Objetos con estado `Sin uso interno identificado` o `Referencia rota`. Su detalle está en la sección de origen; aquí solo lo que "
      "necesita el DLC de depuración. Aprobación de todas: **Pendiente; el CENSO no autoriza eliminar** (R27). Los objetos `En uso` y "
      "`Uso técnico` se consideran protegidos. Los formatos huérfanos no son candidatos: su visual funciona.\n")
    cand = candidatas(inv, a)
    tipos = sorted({r[1] for r in cand})
    w("Riesgo y pruebas por defecto según el tipo de objeto (la IA puede precisarlos en la columna «Nota» de cada fila):\n")
    w(tabla(["Tipo", "Riesgo por defecto", "Pruebas sugeridas"], [[t, RIESGO[t], PRUEBAS[t]] for t in tipos]))
    w(tabla(["#", "Tipo", "Objeto", "ID", "Sección", "Estado de uso", "Nota"], cand, num=("#",)))

    # ---------------------------------------------------------------- 18
    w("# 18. Validación final\n")
    w("## 18.1 Conciliación contra el PBIP\n")
    ncol = sum(len(t["columnas"]) for t in tablas)
    w(tabla(["Inventario", "En PBIP", "En este documento", "Diferencia"], [
        ["Tablas", len(tablas), len(reales) + len(autos), 0], ["Columnas", ncol, ncol, 0],
        ["Medidas", sum(len(t["medidas"]) for t in tablas), len(allm), 0], ["Relaciones", len(inv.get("relaciones", [])), len(inv.get("relaciones", [])), 0],
        ["Páginas", len(pages), len(pages), 0], ["Visuales", len(vis), len(vis), 0], ["Filtros", len(flt), len(flt), 0],
        ["Segmentaciones", len(sl), len(sl), 0], ["Interacciones", len(it), len(it), 0], ["Bookmarks", len(bks), len(bks), 0],
        ["Recursos", len(rec), len(rec), 0]], num=("En PBIP", "En este documento", "Diferencia")))
    w("`censo.py validar` recalcula esta tabla desde el documento y el PBIP. El resultado de la validación queda en `historial-censos.md`.\n")
    w("## 18.2 Estado final\n\n[IA: 1–3 frases que justifiquen el estado del encabezado según CAT-07.]\n")
    return "\n".join(L)


def _fila_disenio(zona, v, banda, vi, rec_by):
    info = vi[(v["page_id"], v["visual_id"])]
    if banda is not None and v["visual_id"] == banda["visual_id"]:
        rol = "Fondo del banner"
    elif v["tipo"] == "image" or v.get("recurso"):
        rol = "Logo / imagen"
    elif v["tipo"] in ("shape", "basicShape"):
        rol = "Separador / forma" if min(v["ancho"] or 0, v["alto"] or 0) <= 20 else "Forma / fondo de bloque"
    elif v["tipo"] == "textbox":
        rol = "Título / texto"
    elif v["tipo"] == "actionButton":
        rol = "Botón"
    else:
        rol = "Contenido: " + TIPO_LEGIBLE.get(v["tipo"], v["tipo"])
    img = "—"
    if v.get("recurso"):
        r = rec_by.get(v["recurso"], {})
        orig = f"{r.get('ancho')}×{r.get('alto')}" if r.get("ancho") else "?"
        esc = f" ({round(100 * (v['ancho'] or 0) / r['ancho'])} %)" if r.get("ancho") else ""
        img = f"{v['recurso']} · {orig} → {v['ancho']}×{v['alto']}{esc} · {r.get('ruta', '—')}"
    return [zona, v["visual_id"], info["nombre"], rol, v["x"], v["y"], v["ancho"], v["alto"], v["z"], v["oculto"], img]


def vacios(args):
    d = args.correo_dueno_tablero
    base = [("Frecuencia y proceso de actualización", "Vigencia del dato", "El PBIP no guarda la programación de refresco"),
            ("Ambiente y workspace de publicación", "Dónde se consume", "Sin evidencia en el PBIP"),
            ("Propietario de cada fuente de la sección 3", "Gobierno del dato", "No está en el PBIP")]
    return [[f"V-A{i:02d}", "Vacío", "Gobierno", f"No se conoce: {x}.", "BI", "—", "—", "—", ev, "Desconocido", "—", imp, "Media",
             "Confirmar con el dueño.", f"Sí ({d})", "Pendiente de validación"] for i, (x, imp, ev) in enumerate(base, 1)]


def hallazgos(inv, a, pname, vn, bn):
    rows, n = [], 0

    def add(tipo, cat, desc, pag, pid, oid, bk, ev, afect, imp, prio, punto):
        nonlocal n
        n += 1
        rows.append([f"H-A{n:02d}", tipo, cat, desc, pag, pid, oid, bk, ev, "Encontrado", afect, imp, prio, punto, "Sí", "Pendiente de validación"])

    by_ent = defaultdict(dict)
    for v, b in a["broken_bindings"]:
        by_ent[b["tabla"]][(v["page_id"], v["visual_id"])] = v
    for ent, uniq in by_ent.items():
        ocultos = sum(1 for v in uniq.values() if v["oculto"])
        add("Riesgo", "Referencias", f"{len(uniq)} visuales ({ocultos} ocultos) muestran datos de la entidad «{ent}», que no existe en el modelo; "
            "no pueden dibujarse.", ", ".join(sorted({pname.get(p, p) for p, _ in uniq})), ", ".join(sorted({p for p, _ in uniq})),
            "; ".join(vn(v) for _, v in uniq), "—", "Bindings de datos en visual.json (sección 9)", "Bookmarks de 12.2 que los incluyen",
            "Mantenimiento y confusión; error si se muestran", "Media", f"Validar con el dueño si los visuales que usan «{ent}» pertenecen a este tablero.")
    of = defaultdict(dict)
    for v, ent, prop in a["orphan_formats"]:
        of[(v["page_id"], v["visual_id"])][ent] = v
    if of:
        ents = sorted({e for d in of.values() for e in d})
        funcionan = [k for k in of if not a["visual_info"][k]["rota"]]
        rotos = len(of) - len(funcionan)
    if of and funcionan:
        add("Observación", "Presentación", (f"1 visual que funciona conserva reglas de formato que apuntan a entidades " if len(funcionan) == 1 else
         f"{len(funcionan)} visuales que funcionan conservan reglas de formato que apuntan a entidades ") +
        f"inexistentes ({', '.join(ents)}). Otros {rotos} visuales con formato huérfano ya están rotos por sus datos y se cubren en los "
            "hallazgos de referencias; todos figuran como «Formato huérfano» en los bindings de la sección 9.",
            ", ".join(sorted({pname.get(p, p) for p, _ in funcionan})), ", ".join(sorted({p for p, _ in funcionan})),
            "; ".join(vn(v) for _, v in funcionan), "—",
            "Filas «Formato huérfano» en los bindings (sección 9)", "Ninguno: la regla no se aplica", "Bajo: no afecta los datos mostrados", "Baja",
            "Revisar con el dueño si estos formatos heredados de la plantilla deben conservarse.")
    ph = a["phantom_pages"]
    bk_ph = [b for b in inv.get("bookmarks", []) if b["seccion"] in ph]
    if bk_ph:
        add("Riesgo", "Referencias", f"{len(bk_ph)} bookmarks apuntan a páginas que no existen ({', '.join(sorted({b['seccion'] for b in bk_ph}))}).",
            "Reporte", "—", "; ".join(bn(b["bookmark_id"]) for b in bk_ph), "activeSection", "bookmark.json (sección 12.1)",
            "Botones o navegadores que los invoquen (12.4)", "Navegación sin destino", "Media",
            "Validar visualmente en Power BI qué ocurre al activar estos bookmarks.")
    bk_r = [b for b in inv.get("bookmarks", []) if b["seccion"] not in ph and b["estado"] == "Referencia rota"]
    if bk_r:
        add("Riesgo", "Referencias", f"{len(bk_r)} bookmarks de páginas existentes solo actúan sobre visuales rotos o inexistentes: al activarlos "
            "muestran u ocultan visuales que no funcionan.", "Reporte", ", ".join(sorted({b["seccion"] for b in bk_r})),
            "; ".join(bn(b["bookmark_id"]) for b in bk_r), "Targets (12.2)", "bookmark.json (sección 12.2)", "Visuales rotos de la sección 9",
            "Puede mostrar mensajes de error al usuario", "Media", "Validar visualmente en Power BI cada bookmark con el dueño.")
    bk_t = [b for b in inv.get("bookmarks", []) if b["seccion"] not in ph and b["estado"] != "Referencia rota" and any(not d["existe"] for d in b["targets_detalle"])]
    if bk_t:
        add("Observación", "Referencias", f"{len(bk_t)} bookmarks tienen además algún target que no existe en el PBIP.", "Reporte",
            ", ".join(sorted({b["seccion"] for b in bk_t})), "; ".join(bn(b["bookmark_id"]) for b in bk_t), "targetVisualNames",
            "bookmark.json (12.2)", "—", "Bajo", "Baja", "Revisar con el dueño si estos bookmarks siguen en uso.")
    for v in inv.get("visuales", []):
        for ac in v["acciones"]:
            dest = ac.get("navigationSection") or ac.get("drillthroughSection")
            if dest and dest in ph:
                add("Riesgo", "Referencias", f"El botón «{a['visual_info'][(v['page_id'], v['visual_id'])]['nombre']}» navega a la página {dest}, que no existe.",
                    pname.get(v["page_id"]), v["page_id"], vn(v["visual_id"]), bn(ac.get("bookmark")), "visualLink en visual.json (12.4)",
                    "Bookmark asociado: " + bn(ac.get("bookmark")), "Botón sin destino", "Media", "Validar visualmente en Power BI a dónde lleva el botón.")
    vac = [(t, m) for (t, m), r in a["meas_rows"].items() if "Sin expresión" in r["nota"]]
    if vac:
        add("Observación", "Modelo", f"Medidas sin expresión: {', '.join(m for _, m in vac)}.", "Modelo", "—",
            "; ".join(f"{a['meas'][k]['measure_id']} · {k[1]}" for k in vac), "—", "TMDL (sección 7)", "Ninguno", "Bajo", "Baja",
            "Confirmar con el dueño si estas medidas se necesitan.")
    dup = sorted({tuple(sorted([m] + r["nota"].split("Misma expresión que ")[1].split(";")[0].split(", "))) for (t, m), r in a["meas_rows"].items()
                  if "Misma expresión que" in r["nota"]})
    for g in dup:
        add("Observación", "Modelo", f"Medidas con la misma expresión: {', '.join(g)}.", "Modelo", "—",
            "; ".join(f"{mm['measure_id']} · {m}" for (t, m), mm in a["meas"].items() if m in g), "—", "TMDL (sección 7)",
            "Ver columna «Usa» de la sección 7", "Bajo", "Baja", "Confirmar con el dueño cuál de las medidas es la vigente.")
    seen = defaultdict(list)
    for v in inv.get("visuales", []):
        if (v["tipo"] or "").lower().startswith("slicer") and not v["oculto"]:
            for b in v["bindings"]:
                seen[(v["page_id"], b["tabla"], b["campo"])].append(v["visual_id"])
    for (pid, t, c), ids in seen.items():
        if len(ids) > 1:
            add("Observación", "Reporte", f"{len(ids)} segmentaciones visibles de {ref_txt(t, c)} en la misma página.", pname.get(pid), pid,
                "; ".join(vn(x) for x in ids), "—", "Bindings (sección 9) y 11.2", "Interacciones de 11.3", "Bajo", "Baja",
                "Revisar con el dueño el propósito de cada segmentación.")
    conteos = defaultdict(list)
    for v in inv.get("visuales", []):
        if v["tipo"] in TARJETAS:
            for b in v["bindings"]:
                if b["agregacion"] in ("Count", "CountNonNull") and b.get("estado_ref") == "Válida":
                    conteos[(b["agregacion"], b["tabla"], b["campo"])].append(v)
    for (agg, t, c), vs in conteos.items():
        add("Hallazgo", "Métrica", f"{len(vs)} tarjeta(s) calculan {agg}({ref_txt(t, c)}), un conteo implícito de filas y no una medida.",
            ", ".join(sorted({pname.get(v['page_id']) for v in vs})), ", ".join(sorted({v["page_id"] for v in vs})),
            "; ".join(vn(v["visual_id"]) for v in vs), "—", "Bindings en visual.json (secciones 9 y 10)", f"Columna {ref_txt(t, c)}",
            "El valor puede no corresponder al título de la tarjeta", "Media",
            "Confirmar con el dueño qué debe mostrar cada tarjeta y si el título coincide con lo calculado.")
    p = inv.get("propiedades", {})
    if str(p.get("__PBI_TimeIntelligenceEnabled", "")) == "1":
        autos = [t for t in inv.get("tablas", []) if t["auto"]]
        add("Observación", "Modelo", f"La inteligencia de tiempo automática está activa: {len(autos)} tablas de fecha automáticas.",
            "Modelo", "—", "; ".join(f"{t['table_id']} · {t['tabla']}" for t in autos), "—", "model.tmdl (5.4) y 6.2", "Relaciones de 5.2",
            "Tamaño del modelo", "Baja", "Confirmar con el dueño si se usan las jerarquías de fecha automáticas.")
    for r in inv.get("roles", []):
        if not r["filtros"]:
            add("Observación", "Seguridad", f"El rol «{r['rol']}» no tiene reglas RLS.", "Modelo", "—", r["rol"], "—", r["ruta"], "Todas las tablas",
                "Acceso total a las filas", "Baja", "Confirmar con el dueño si corresponde seguridad por filas.")
    for r in inv.get("recursos", []):
        if r.get("estado") in ("Sin uso interno identificado", "Referencia rota"):
            add("Observación", "Presentación", f"Recurso «{r['resource_id']}»: {r['estado'].lower()}.", "Reporte", "—", r["resource_id"], "—",
                f"{r.get('ruta')} (13.1)", "Ninguno", "Bajo", "Baja", "Revisar con el dueño si el recurso se necesita.")
    for kind, host, name, ref in a["rota_dax"]:
        add("Hallazgo", "Modelo", f"La expresión DAX de {name} referencia {ref}, que no existe.", "Modelo", "—", name, "—", "TMDL (6.1 o 7)",
            "Visuales que usan el objeto", "Error de cálculo", "Alta", "Verificar en Power BI Desktop si el objeto calcula sin error.")
    return rows


RIESGO = {"Columna": "Medio: puede tener uso fuera del PBIP (fuente, otros reportes)", "Columna calculada": "Bajo: sin consumidores en el PBIP",
          "Medida": "Bajo: sin consumidores en el PBIP", "Visual": "Bajo si está oculto; medio si es visible", "Bookmark": "Bajo",
          "Recurso": "Bajo"}
PRUEBAS = {"Columna": "Confirmar con el dueño y con la fuente; comparar totales de visuales antes y después",
           "Columna calculada": "Comparar visuales y medidas antes y después", "Medida": "Abrir todas las páginas y revisar errores",
           "Visual": "Comparar la página en cada bookmark antes y después", "Bookmark": "Probar navegación y botones",
           "Recurso": "Revisar visualmente fondos, logos e íconos"}


def candidatas(inv, a):
    rows = []

    def add(tipo, obj, oid, sec, est):
        rows.append([len(rows) + 1, tipo, obj, oid, sec, est, "—"])

    for (t, c), r in a["col_rows"].items():
        cc = a["cols"][(t, c)]
        if r["estado"] == "Sin uso interno identificado" and not t.startswith(("LocalDateTable_", "DateTableTemplate_")):
            add("Columna calculada" if cc["calculada"] else "Columna", ref_txt(t, c), cc["column_id"], "6.1", r["estado"])
    for (t, m), r in a["meas_rows"].items():
        if r["estado"] == "Sin uso interno identificado":
            add("Medida", f"[{m}]", a["meas"][(t, m)]["measure_id"], "7", r["estado"])
    for v in inv.get("visuales", []):
        info = a["visual_info"][(v["page_id"], v["visual_id"])]
        if info["estado"] == "Referencia rota":
            add("Visual", f"{info['nombre']} ({a['pname'].get(v['page_id'], v['page_id'])})", v["visual_id"], "9", "Referencia rota")
    for b in inv.get("bookmarks", []):
        if b["estado"] == "Referencia rota":
            add("Bookmark", b["nombre"], b["bookmark_id"], "12", "Referencia rota")
    for r in inv.get("recursos", []):
        if r.get("estado") in ("Sin uso interno identificado", "Referencia rota"):
            add("Recurso", r["resource_id"], r["resource_id"], "13.1", r["estado"])
    return rows


# =============================================================================================
# Lectura del Markdown para validar
# =============================================================================================
def split_cells(line):
    parts = re.split(r"(?<!\\)\|", line.strip())
    return [p.strip().replace("\\|", "|") for p in parts[1:-1]]


def md_sections(md):
    secs = {}
    cur, buf = None, []
    for line in md.splitlines():
        m = re.match(r"^# (\d{1,2})\. (.+)$", line)
        if m:
            if cur is not None:
                secs[cur[0]] = (cur[1], buf)
            cur, buf = (int(m.group(1)), m.group(2).strip()), []
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        secs[cur[0]] = (cur[1], buf)
    return secs


def md_tables(lines):
    out, i = [], 0
    while i < len(lines) - 1:
        if lines[i].startswith("|") and re.match(r"^\|\s*:?-", lines[i + 1]):
            hdr = split_cells(lines[i])
            rows, j = [], i + 2
            while j < len(lines) and lines[j].startswith("|"):
                rows.append(split_cells(lines[j]))
                j += 1
            out.append((hdr, rows))
            i = j
        else:
            i += 1
    return out


def col_values(tables, header, require=None):
    vals = []
    for hdr, rows in tables:
        if header in hdr and (require is None or require in hdr):
            k = hdr.index(header)
            vals += [r[k] for r in rows if k < len(r)]
    return vals


def validate(md: str, pbip: Path | None):
    err, warn = [], []
    secs = md_sections(md)
    nums = sorted(secs)
    order = [int(m.group(1)) for m in re.finditer(r"^# (\d{1,2})\. ", md, re.M)]
    if order != list(range(len(SECCIONES))):
        err.append(f"Secciones: se esperan 0–{len(SECCIONES) - 1} en orden; encontradas {order}.")
    for n in nums:
        if n < len(SECCIONES) and not secs[n][0].lower().startswith(SECCIONES[n].lower()[:12]):
            warn.append(f"Sección {n} titulada «{secs[n][0]}»; se esperaba «{SECCIONES[n]}».")
    lines = md.splitlines()
    for i, line in enumerate(lines, 1):
        for m in IA.finditer(line):
            err.append(f"Línea {i}: marcador pendiente {m.group(0)[:80]}")
        if "[Completar" in line:
            err.append(f"Línea {i}: marcador de plantilla «[Completar]».")
        m = APROX.search(line)
        if m and not line.startswith(("```", "    ")):
            err.append(f"Línea {i}: conteo aproximado «{m.group(0)}» (R17).")
        m = TRUNC.search(line)
        if m:
            err.append(f"Línea {i}: ID truncado «{m.group(0)}» (R12).")
    head = {k: (re.search(rf"^> {k}:\s*(.+)$", md, re.M) or [None, None])[1] for k in ("Estado", "census_id", "Fecha y hora de ejecución", "Tipo de CENSO")}
    if head["Estado"] not in CAT["estado_censo"]:
        err.append(f"Encabezado: estado «{head['Estado']}» fuera de CAT-07.")
    if not head["census_id"] or not CID.match(head["census_id"].strip()):
        err.append(f"Encabezado: census_id «{head['census_id']}» inválido.")
    if not head["Fecha y hora de ejecución"] or not FECHA.match(head["Fecha y hora de ejecución"].strip()):
        err.append("Encabezado: fecha y hora deben ser ISO con zona horaria.")
    if head["Tipo de CENSO"] not in CAT["tipo_censo"]:
        err.append(f"Encabezado: tipo «{head['Tipo de CENSO']}» fuera de CAT-08.")
    for lbl in ("Correo de quien realiza el CENSO", "Correo del dueño/responsable del tablero"):
        m = re.search(rf"\*\*{re.escape(lbl)}:\*\*\s*(\S+)", md)
        if not m or not EMAIL.match(m.group(1)):
            err.append(f"Sección 0: falta un correo válido en «{lbl}» (R02).")
    T = {n: md_tables(secs[n][1]) for n in nums}
    for n, tabs in T.items():
        for hdr, rows in tabs:
            if "Estado de uso" in hdr:
                k = hdr.index("Estado de uso")
                for r in rows:
                    v = r[k] if k < len(r) else ""
                    if v not in CAT["estado_uso"] and not (n == 6 and "," in v):
                        err.append(f"Sección {n}: estado de uso «{v}» fuera de CAT-02 (fila {r[0]}).")
            present = [c for c in CLASES if c in hdr]
            if present and "Estado de uso" in hdr and "column_id" in hdr:
                for r in rows:
                    vals = {c: r[hdr.index(c)] for c in present}
                    for c, v in vals.items():
                        if not re.fullmatch(r"\d+|NA|NV|P", v):
                            err.append(f"Sección 6: valor «{v}» en clase {c} de {r[1]} (use número, NA, NV o P).")
                    if r[hdr.index("Estado de uso")] == "Sin uso interno identificado":
                        bad = [c for c in OBLIGATORIAS if c in vals and vals[c] not in ("0", "NA")]
                        if bad:
                            err.append(f"Sección 6: {r[1]} está «Sin uso interno identificado» con clases {bad} no revisadas o con referencias (R22).")
    for hdr, rows in T.get(16, []):
        if "Punto de revisión" not in hdr:
            continue
        ix = {h: i for i, h in enumerate(hdr)}
        for r in rows:
            g = lambda h: r[ix[h]] if h in ix and ix[h] < len(r) else ""  # noqa: E731
            for h, cat in (("Tipo", "tipo_hallazgo"), ("Prioridad", "prioridad"), ("Estado", "estado_punto"), ("Certeza", "certeza")):
                if g(h) not in CAT[cat]:
                    err.append(f"Sección 16 {r[0]}: {h} «{g(h)}» fuera de catálogo.")
            m = VERBOS.search(g("Punto de revisión"))
            if m:
                err.append(f"Sección 16 {r[0]}: verbo de cambio «{m.group(0)}» en el punto de revisión (R47).")
            if not re.match(r"^[HV]-A\d+$", r[0]):
                citas = sorted({x for c in r[1:] for x in re.findall(r"\b[HV]-A\d{2}\b", c)})
                if citas:
                    err.append(f"Sección 16 {r[0]}: cita {', '.join(citas)}; si es el mismo asunto, ajuste esa fila en vez de crear otra (R45).")
    if 17 in secs:
        lim = []
        for line in secs[17][1]:
            if line.startswith("## 17.2"):
                break
            m = re.match(r"^(\d+)\. (.*)$", line)
            if m:
                lim.append((int(m.group(1)), m.group(2)))
        std = lim[:LIM_ESTANDAR]
        for n_, txt in lim[LIM_ESTANDAR:]:
            if re.search(r"\b[HV]-A?\d{2}\b", txt):
                err.append(f"Sección 17.1, limitación {n_}: cita un hallazgo o vacío; los problemas del tablero van solo en la sección 16 (R49).")
            a_ = _palabras(txt)
            for m_, base in std:
                b_ = _palabras(base)
                if a_ and b_ and len(a_ & b_) / min(len(a_), len(b_)) >= 0.5:
                    warn.append(f"Sección 17.1, limitación {n_}: se parece a la limitación estándar {m_} "
                                f"(comparten: {', '.join(sorted(a_ & b_))}); si dice lo mismo, quítela (R49).")
                    break
    if 6 in secs and 14 in secs:  # R51: interpretación coherente con 6.1
        est, tb = {}, None
        for line in secs[6][1]:
            m = re.match(r"^### (.+?) \(\d+ columnas\)", line)
            if m:
                tb = m.group(1)
            elif tb and line.startswith("| ") and not line.startswith("| column_id") and not line.startswith("|---"):
                c = split_cells(line)
                if len(c) >= 15 and c[-2] in CAT["estado_uso"]:
                    est[f"{tb}[{c[1]}]"] = c[-2]
        for h, rows in md_tables(secs[14][1]):
            if "rule_id" not in h:
                continue
            for r in rows:
                m = re.match(r"^`?([^`\[]+\[[^\]]+\])`? \(6\.1\)", r[2])
                if not m or r[3] in ("—", ""):
                    continue
                ref = m.group(1)
                if est.get(ref) == "Sin uso interno identificado" and "sin uso" not in r[3].lower():
                    warn.append(f"Sección 14, {r[0]}: {ref} figura «Sin uso interno identificado» en 6.1, pero la interpretación no lo dice; "
                                "no describa un uso que el censo no encontró (R51).")
                if r[4].startswith("Encontrado") and "Inferido" not in r[4]:
                    warn.append(f"Sección 14, {r[0]}: la expresión de {ref} está en 6.1, pero su significado de negocio es Inferido; "
                                "use «Inferido» salvo que el PBIP lo documente (R51).")
    if pbip:
        inv = read_pbip(pbip)
        def comp(label, src, dst):
            src, dst = set(src), set(dst)
            if src - dst:
                err.append(f"Conciliación {label}: {len(src - dst)} en el PBIP sin registro en el documento: {sorted(src - dst)[:6]}")
            if dst - src:
                err.append(f"Conciliación {label}: {len(dst - src)} en el documento que no existen en el PBIP: {sorted(dst - src)[:6]}")
        comp("visuales", [v["visual_id"] for v in inv["visuales"]], col_values(T.get(9, []), "visual_id", "Tipo"))
        comp("páginas", [p["page_id"] for p in inv["paginas"]], col_values(T.get(8, []), "page_id", "Página"))
        auto_ids = [x.split("=", 1)[1] for s in col_values(T.get(6, []), "column_id por columna") for x in s.split("; ") if "=" in x]
        comp("columnas", [c["column_id"] for t in inv["tablas"] for c in t["columnas"]], col_values(T.get(6, []), "column_id") + auto_ids)
        comp("medidas", [m["measure_id"] for t in inv["tablas"] for m in t["medidas"]], col_values(T.get(7, []), "measure_id"))
        comp("tablas", [t["table_id"] for t in inv["tablas"]], col_values(T.get(5, []), "table_id") + col_values(T.get(6, []), "table_id"))
        comp("relaciones", [r["relationship_id"] for r in inv["relaciones"]], col_values(T.get(5, []), "relationship_id"))
        comp("bookmarks", [b["bookmark_id"] for b in inv["bookmarks"]], col_values(T.get(12, []), "bookmark_id", "Nombre"))
        comp("recursos", [r["resource_id"] for r in inv["recursos"]], col_values(T.get(13, []), "resource_id"))
        nf = len(col_values(T.get(11, []), "filter_id"))
        if nf != len(inv["filtros"]):
            err.append(f"Conciliación filtros: PBIP {len(inv['filtros'])}, documento {nf}.")
        ni = len(col_values(T.get(11, []), "Visual origen"))
        if ni != len(inv["interacciones"]):
            err.append(f"Conciliación interacciones: PBIP {len(inv['interacciones'])}, documento {ni}.")
        hu = cv.leer_huella(md)
        if hu and hu != cv.huella(pbip)[0]:
            err.append("Huella del PBIP distinta a la del censo: el tablero se modificó o se guardó después del borrador. "
                       "Guarde la versión y ejecute un censo nuevo (R53).")
    else:
        warn.append("Sin --pbip no se concilia contra la fuente; no use «Completado y validado».")
        if head["Estado"] == "Completado y validado":
            err.append("«Completado y validado» exige validar con --pbip.")
    if not cv.leer_huella(md):
        warn.append("El encabezado no tiene «Huella del PBIP» (censo anterior a v2.3): `vigencia` no podrá confirmarlo; "
                    "se agrega con `iniciar-validacion` o con un censo nuevo (R53).")
    mails = re.findall(r"\*\*Correo[^*]+:\*\*\s*(\S+)", md)
    mismo = len(mails) > 1 and mails[0].lower() == mails[1].lower()
    pend = []
    for hdr, rows in T.get(14, []):
        if "rule_id" not in hdr or "Validación del dueño" not in hdr:
            continue
        ix = {h: i for i, h in enumerate(hdr)}
        for r in rows:
            val, cer = r[ix["Validación del dueño"]], r[ix["Certeza"]]
            resp = r[ix["Respuesta del dueño"]] if "Respuesta del dueño" in ix else "—"
            if val not in CAT["estado_punto"] | {"No requerida"}:
                err.append(f"Sección 14, {r[0]}: «Validación del dueño» = «{val}» (use «No requerida» o un valor de CAT-12).")
            elif val == "No requerida" and "Inferido" in cer:
                err.append(f"Sección 14, {r[0]}: es Inferida y no puede ser «No requerida»; queda «Pendiente de validación» hasta que el dueño responda (R55).")
            if val in cv.RESUELTOS and resp in ("—", ""):
                err.append(f"Sección 14, {r[0]}: «{val}» sin respuesta del dueño registrada (R55).")
            if val == cv.PENDIENTE:
                pend.append((14, r[0], resp))
    for hdr, rows in T.get(16, []):
        if "Punto de revisión" not in hdr:
            continue
        ix = {h: i for i, h in enumerate(hdr)}
        for r in rows:
            est = r[ix["Estado"]]
            resp = r[ix["Respuesta del dueño"]] if "Respuesta del dueño" in ix else "—"
            if est in cv.RESUELTOS and resp in ("—", ""):
                err.append(f"Sección 16, {r[0]}: «{est}» sin respuesta del dueño registrada (R55).")
            if est == cv.PENDIENTE:
                pend.append((16, r[0], resp))
    tipo_ = head.get("Tipo de CENSO")
    delegada = "**Validación sin ser el dueño:** Sí" in md
    if tipo_ == "Validación" and not mismo and not delegada:
        err.append("Validación hecha por alguien que no es el dueño sin la aceptación registrada en la sección 0; "
                   "use `iniciar-validacion --acepta-validar-sin-ser-dueno` (R58).")
    if mismo or tipo_ == "Validación":
        sin = [f"{n}·{i}" for n, i, resp in pend if resp in ("—", "")]
        if sin:
            err.append(f"{'Quien realiza el censo es el dueño' if mismo else 'En una Validación'}: cada punto pendiente debe tener su respuesta o la constancia de que se "
                       f"preguntó (R55, R58). Sin respuesta: {', '.join(sin[:12])}{' …' if len(sin) > 12 else ''}")
    if head["Estado"] == "Completado y validado" and pend:
        err.append(f"«Completado y validado» exige que no queden puntos «Pendiente de validación» en 14 y 16 (R56); quedan {len(pend)}.")
    return err, warn, head


# =============================================================================================
# CLI
# =============================================================================================
LIM_ESTANDAR = 5  # limitaciones que escribe el script en 17.1
_STOP = {"para", "como", "esta", "este", "estos", "esas", "esos", "solo", "sobre", "entre", "desde", "pero", "porque", "queda",
         "sujeto", "directamente", "tablero", "censo"}


def _palabras(t):
    import unicodedata
    t = unicodedata.normalize("NFKD", t.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return {w for w in re.findall(r"[a-z]{4,}", t) if w not in _STOP}


def need_emails(args):
    bad = [l for l, v in (("--correo-ejecutor", args.correo_ejecutor), ("--correo-dueno-tablero", args.correo_dueno_tablero))
           if not v or not EMAIL.match(v.strip())]
    if bad:
        print("CENSO BLOQUEADO (R02): faltan correos válidos en " + ", ".join(bad) + ".", file=sys.stderr)
        sys.exit(2)


def report(err, warn):
    for x in warn:
        print("ADVERTENCIA: " + x)
    for x in err:
        print("ERROR: " + x)
    print(f"Errores: {len(err)} · Advertencias: {len(warn)}")


def _rutas(md_path: Path):
    """Rutas del censo vigente, borradores, registro de cambios y archivo de versiones a partir de cualquier archivo del BI."""
    base = md_path.name.replace(" - censo.borrador.md", "").replace(" - censo.md", "")
    d = md_path.parent
    return {"bi": base, "vigente": d / f"{base} - censo.md", "borrador": d / f"{base} - censo.borrador.md",
            "cambios": d / f"{base} - cambios.md", "cambios_b": d / f"{base} - cambios.borrador.md",
            "versiones": d / "versiones", "historial": d / "historial-censos.md"}


def _ids(md):
    return set(re.findall(r"\b[0-9a-f]{20}\b|\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", md))


def _historial(hist: Path, valores: dict):
    hdr = ["census_id", "Fecha y hora de ejecución", "Tipo", "Versión analizada", "Huella del PBIP", "census_id anterior", "Alcance",
           "Correo ejecutor", "Correo dueño", "Estado", "Pendientes de validación", "Archivo", "Versión del ritual", "Validador", "Observaciones"]
    if hist.exists():
        for line in hist.read_text(encoding="utf-8").splitlines():
            if line.startswith("| census_id |"):
                hdr = split_cells(line)
                break
    else:
        hist.write_text("# Historial de ejecuciones del CENSO\n\nAppend-only (R38): no editar ni borrar filas.\n\n"
                        "| " + " | ".join(hdr) + " |\n|" + "|".join("---" for _ in hdr) + "|\n", encoding="utf-8")
    with hist.open("a", encoding="utf-8") as fh:
        fh.write("| " + " | ".join(cell(valores.get(h, "—")) for h in hdr) + " |\n")


def _dueno(md: str):
    m = re.search(r"\*\*Correo del dueño/responsable del tablero:\*\*\s*(\S+)", md)
    return m.group(1).strip().lower() if m else None


def _revisor(args, md: str):
    """Correo de quien revisa (R57). Devuelve (correo, rol)."""
    c = (getattr(args, "correo_revisor", None) or "").strip().lower()
    if not EMAIL.match(c):
        print("REVISIÓN BLOQUEADA (R57): indique el correo de quien revisa el censo con --correo-revisor.", file=sys.stderr)
        sys.exit(2)
    return c, ("dueño del tablero" if c == _dueno(md) else "no es el dueño")


def _log_revision(md_path: Path, correo: str, rol: str, comando: str, cid, resultado: str):
    """Agrega una fila a revisiones-censo.md de la carpeta del BI (append-only, R57). No registra en examples/."""
    if md_path.parent.name == "examples":
        return
    f = md_path.parent / "revisiones-censo.md"
    if not f.exists():
        f.write_text("# Registro de revisiones del CENSO\n\nAppend-only (R57): una fila por consulta o revisión de un censo de esta carpeta.\n\n"
                     "| Fecha y hora | Correo de quien revisa | Rol | Comando | census_id | Resultado |\n|---|---|---|---|---|---|\n", encoding="utf-8")
    with f.open("a", encoding="utf-8") as fh:
        fh.write("| " + " | ".join(cell(x) for x in (datetime.now().astimezone().isoformat(timespec="seconds"), correo, rol, comando,
                                                       cid or "—", resultado)) + " |\n")


def fichas_validacion(md: str):
    """Datos de cada punto «Pendiente de validación» (14 y 16), ordenados para presentarlos uno por uno (R59)."""
    secs, lines = md_sections(md), md.split("\n")
    def linea(rid):
        for k, l in enumerate(lines, 1):
            if l.startswith(f"| {rid} |"):
                return k
        return 0
    orden = {"Alta": 0, "Media": 2, "Baja": 3}
    out = []
    for hdr, rows in md_tables(secs.get(16, ("", []))[1]):
        if "Punto de revisión" not in hdr:
            continue
        g = lambda r, c: r[hdr.index(c)] if c in hdr else "—"  # noqa: E731
        for r in rows:
            if g(r, "Estado") != "Pendiente de validación":
                continue
            out.append((orden.get(g(r, "Prioridad"), 2), {
                "ID": r[0], "Sección": "16", "Línea": linea(r[0]), "Tipo": g(r, "Tipo"), "Categoría": g(r, "Categoría"),
                "Prioridad": g(r, "Prioridad"), "Qué se encontró": g(r, "Descripción concreta"),
                "Dónde": g(r, "Página y objeto") + (f" · objetos: {g(r, 'visual_id / object_id (con nombre)')}" if g(r, "visual_id / object_id (con nombre)") != "—" else ""),
                "Evidencia": g(r, "Evidencia exacta") + f" (certeza: {g(r, 'Certeza')})", "Qué depende de esto": g(r, "Objetos afectados y dependencias"),
                "Impacto": g(r, "Impacto"), "Qué hay que confirmar": g(r, "Punto de revisión")}))
    for hdr, rows in md_tables(secs.get(14, ("", []))[1]):
        if "rule_id" not in hdr or "Validación del dueño" not in hdr:
            continue
        for r in rows:
            if r[hdr.index("Validación del dueño")] != "Pendiente de validación":
                continue
            out.append((1, {"ID": r[0], "Sección": "14", "Línea": linea(r[0]), "Tipo": "Regla de negocio inferida", "Categoría": "Regla de negocio",
                            "Prioridad": "—", "Qué se encontró": r[1], "Dónde": r[2], "Evidencia": f"{r[2]} (certeza: {r[4]})",
                            "Qué depende de esto": "—", "Impacto": "Si la interpretación no es correcta, los cortes y KPIs que usan esta regla se leerían con otro significado.",
                            "Qué hay que confirmar": "¿Es correcta esta interpretación? " + r[3]}))
    return [x for _, x in sorted(out, key=lambda x: x[0])]


def main():
    ap = argparse.ArgumentParser(description=f"CENSO BI — ritual AI-DLC v{RITUAL}")
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("borrador")
    b.add_argument("--pbip", type=Path, required=True)
    b.add_argument("--salida", type=Path, required=True)
    b.add_argument("--version", required=True)
    b.add_argument("--tipo", required=True, choices=sorted(CAT["tipo_censo"]))
    b.add_argument("--census-anterior")
    b.add_argument("--pbip-guardado-confirmado", action="store_true",
                   help="Obligatorio en Actualización: el usuario confirmó que guardó el PBIP de la versión nueva en la ruta indicada (R54).")
    b.add_argument("--correo-ejecutor")
    b.add_argument("--correo-dueno-tablero")
    pe = sub.add_parser("pendientes")
    pe.add_argument("--markdown", type=Path, required=True)
    pe.add_argument("--correo-revisor", required=True, help="Correo de quien revisa (R57)")
    c = sub.add_parser("comparar")
    c.add_argument("--borrador", type=Path, required=True)
    c.add_argument("--origen", required=True,
                   help="Origen del cambio: «DLC de modificación <ID>», «DLC de depuración <ID>», «Validación con el dueño» o «No informado».")
    iv = sub.add_parser("iniciar-validacion")
    iv.add_argument("--markdown", type=Path, required=True, help="Censo vigente")
    iv.add_argument("--pbip", type=Path, required=True)
    iv.add_argument("--correo-revisor", required=True, help="Correo de quien inicia la validación (R57)")
    iv.add_argument("--acepta-validar-sin-ser-dueno", action="store_true",
                    help="La persona, sin ser el dueño, confirmó que conoce las respuestas y acepta iniciar la validación (R58)")
    gv = sub.add_parser("guia-validacion")
    gv.add_argument("--markdown", type=Path, required=True, help="Censo o borrador de validación")
    gv.add_argument("--correo-revisor", required=True, help="Correo de quien revisa (R57)")
    v = sub.add_parser("validar")
    v.add_argument("--markdown", type=Path, required=True)
    v.add_argument("--pbip", type=Path)
    v.add_argument("--correo-revisor", required=True, help="Correo de quien revisa (R57)")
    r = sub.add_parser("registrar")
    r.add_argument("--markdown", type=Path, required=True)
    r.add_argument("--pbip", type=Path, required=True)
    r.add_argument("--alcance", default="Censo completo del PBIP con censo.py")
    r.add_argument("--observaciones", default="")
    vg = sub.add_parser("vigencia")
    vg.add_argument("--markdown", type=Path, required=True, help="Censo vigente")
    vg.add_argument("--versiones", type=Path, required=True, help="Carpeta 01_bi/01_versiones")
    vg.add_argument("--correo-revisor", required=True, help="Correo de quien revisa (R57)")
    i = sub.add_parser("inventario")
    i.add_argument("--pbip", type=Path, required=True)
    i.add_argument("--salida-json", type=Path, required=True)
    args = ap.parse_args()

    if args.cmd == "borrador":
        need_emails(args)
        if not args.pbip.is_dir() or not any(args.pbip.glob("*.pbip")):
            sys.exit(f"CENSO BLOQUEADO (R54): no hay un PBIP guardado en {args.pbip} (falta la carpeta o el archivo .pbip).")
        bi = args.pbip.name
        R_ = _rutas(args.salida / f"{bi} - censo.md")
        if args.tipo == "Validación":
            sys.exit("Una Validación no genera borrador: use `censo.py iniciar-validacion --markdown <censo vigente> --pbip <PBIP>` (R55).")
        args.huella, args.huella_n = cv.huella(args.pbip)
        if args.tipo == "Inicial" and R_["vigente"].exists():
            sys.exit("Ya existe un censo de este BI: use --tipo Actualización (versión nueva del PBIP) o `iniciar-validacion` (mismo PBIP).")
        if args.tipo == "Actualización":
            if not R_["vigente"].exists():
                sys.exit("No hay censo vigente que actualizar: use --tipo Inicial.")
            if not args.pbip_guardado_confirmado:
                sys.exit(f"CENSO BLOQUEADO (R54): confirme con el usuario que guardó el PBIP de la versión «{args.version}» en {args.pbip} "
                         "y repita el comando con --pbip-guardado-confirmado.")
            if args.pbip.parent.name != args.version:
                sys.exit(f"CENSO BLOQUEADO (R54): la ruta del PBIP está en la carpeta «{args.pbip.parent.name}», pero --version es "
                         f"«{args.version}». Cada versión se guarda en 01_versiones/<versión>/<BI>.")
            vig = R_["vigente"].read_text(encoding="utf-8")
            if cv.cabecera(vig, "Versión analizada") == args.version:
                sys.exit(f"CENSO BLOQUEADO (R54): la versión «{args.version}» ya está censada. Si el PBIP cambió, guárdelo como una versión "
                         "nueva en 01_versiones; si no cambió, use `iniciar-validacion`.")
            if cv.leer_huella(vig) == args.huella:
                sys.exit("CENSO BLOQUEADO (R54): el PBIP de la versión nueva es idéntico al del censo vigente (misma huella). "
                         "Confirme que guardó los cambios en la ruta de la versión nueva.")
            args.census_anterior = args.census_anterior or cv.cabecera(vig, "census_id")
        inv = read_pbip(args.pbip)
        an = analyze(inv)
        now = datetime.now().astimezone()
        census_id = now.strftime("%Y%m%dT%H%M%S-") + (re.sub(r"[^a-z0-9]+", "-", bi.lower()).strip("-") or "bi")
        md = render(inv, an, args, census_id, now.isoformat(timespec="seconds"))
        args.salida.mkdir(parents=True, exist_ok=True)
        dst = R_["borrador"] if R_["vigente"].exists() else R_["vigente"]
        if dst.exists():
            sys.exit(f"Ya hay un borrador sin cerrar: {dst.name}. Ciérrelo con `registrar` o bórrelo a mano antes de generar otro.")
        dst.write_text(md, encoding="utf-8")
        print(f"Borrador escrito: {dst}")
        print(f"Tamaño: {len(md.encode()) // 1024} KB · {md.count(chr(10))} líneas · marcadores [IA] pendientes: {len(IA.findall(md))}")
        print(f"Objetos: {len(inv['visuales'])} visuales, {sum(len(t['columnas']) for t in inv['tablas'])} columnas, "
              f"{sum(len(t['medidas']) for t in inv['tablas'])} medidas, {len(inv['bookmarks'])} bookmarks, {len(inv['recursos'])} recursos.")
        if dst == R_["borrador"]:
            print(f"Siguiente paso: python scripts/censo.py comparar --borrador \"{dst}\" --origen \"...\"")
        else:
            print(f"Siguiente paso: python scripts/censo.py pendientes --markdown \"{dst}\"")
    elif args.cmd == "iniciar-validacion":
        R_ = _rutas(args.markdown)
        if R_["borrador"].exists():
            sys.exit(f"Ya hay un borrador sin cerrar: {R_['borrador'].name}.")
        md = R_["vigente"].read_text(encoding="utf-8")
        correo, rol = _revisor(args, md)
        dueno = _dueno(md)
        if rol != "dueño del tablero" and not args.acepta_validar_sin_ser_dueno:
            _log_revision(R_["vigente"], correo, rol, "iniciar-validacion", cv.cabecera(md, "census_id"), "Bloqueada: sin aceptación (R58)")
            sys.exit(f"VALIDACIÓN BLOQUEADA (R58): {correo} no es el dueño del tablero ({dueno}). Pregunte a la persona si conoce las "
                     "respuestas de los puntos pendientes y si acepta iniciar la validación sin ser el dueño; solo con su aceptación, "
                     "repita el comando con --acepta-validar-sin-ser-dueno.")
        hu, n_ = cv.huella(args.pbip)
        prev = cv.leer_huella(md)
        if prev and prev != hu:
            sys.exit("El PBIP cambió respecto al censo vigente (huella distinta): corresponde un censo de tipo Actualización, no una Validación (R53).")
        now = datetime.now().astimezone()
        cid_old = cv.cabecera(md, "census_id")
        cid = now.strftime("%Y%m%dT%H%M%S-") + cid_old.split("-", 1)[1]
        md = re.sub(r"^> Estado:.*$", "> Estado: [IA: valor de CAT-07 al cerrar la validación]", md, count=1, flags=re.M)
        md = re.sub(r"^> census_id:.*$", f"> census_id: {cid}", md, count=1, flags=re.M)
        md = re.sub(r"^> Fecha y hora de ejecución:.*$", f"> Fecha y hora de ejecución: {now.isoformat(timespec='seconds')}", md, count=1, flags=re.M)
        md = re.sub(r"^> Tipo de CENSO:.*$", "> Tipo de CENSO: Validación", md, count=1, flags=re.M)
        md = re.sub(r"^> Versión del ritual:.*$", f"> Versión del ritual: {RITUAL}", md, count=1, flags=re.M)
        md = re.sub(r"^- \*\*Correo de quien realiza el CENSO:\*\*.*$", f"- **Correo de quien realiza el CENSO:** {correo}", md, count=1, flags=re.M)
        if rol != "dueño del tablero":
            md = re.sub(r"^(- \*\*Correo del dueño/responsable del tablero:\*\*.*)$",
                        rf"\1\n- **Validación sin ser el dueño:** Sí — {correo} declaró conocer las respuestas y aceptó iniciar la validación "
                        rf"sin ser el dueño ({now.isoformat(timespec='seconds')}) (R58).", md, count=1, flags=re.M)
        if not prev:
            md = re.sub(r"^(> Versión analizada:.*\n>)$", rf"\1\n> Huella del PBIP: {hu} ({n_} archivos)\n>", md, count=1, flags=re.M)
        md = re.sub(r"^\| census_id \| [^|]+ \|$", f"| census_id | {cid} |", md, count=1, flags=re.M)
        md = re.sub(r"^\| census_id del censo anterior \| [^|]+ \|$", f"| census_id del censo anterior | {cid_old} |", md, count=1, flags=re.M)
        md = re.sub(r"(## 18\.2 Estado final\n\n)[\s\S]*?(?=\n# |\Z)", r"\1[IA: 1–3 frases que justifiquen el estado tras la validación con el dueño.]\n", md, count=1)
        R_["borrador"].write_text(md, encoding="utf-8")
        p = cv.pendientes_validacion(md, md_sections, md_tables)
        _log_revision(R_["vigente"], correo, rol, "iniciar-validacion", cid,
                      f"Validación iniciada por el dueño; {len(p)} puntos" if rol == "dueño del tablero"
                      else f"Validación iniciada sin ser el dueño (aceptada, R58); {len(p)} puntos")
        print(f"Quien valida: {correo} ({rol}{'; aceptó validar sin ser el dueño' if rol != 'dueño del tablero' else ''})")
        print(f"Borrador de validación: {R_['borrador']}")
        print(f"Puntos por validar con el dueño: {len(p)}")
        for x in p:
            print("  " + x)
        print(f"Siguiente paso: registrar cada respuesta (R55) y luego python scripts/censo.py comparar --borrador \"{R_['borrador']}\" "
              "--origen \"Validación con el dueño\"")
    elif args.cmd == "comparar":
        R_ = _rutas(args.borrador)
        nue = args.borrador.read_text(encoding="utf-8")
        ant = R_["vigente"].read_text(encoding="utf-8")
        if cv.cabecera(nue, "Tipo de CENSO") != "Validación":
            nue, inf = cv.trasladar(ant, nue, md_sections, md_tables, cell, _ids(nue))
            args.borrador.write_text(nue, encoding="utf-8")
            for x in inf:
                print(x)
            guia = cv.guia_marcadores(ant, nue, IA)
            if guia:
                print("Marcadores de la IA: puede reutilizar el texto del censo vigente si los cambios no lo afectan:")
                for x in guia:
                    print("  " + x)
        bloque = cv.bloque_cambios(ant, nue, args.origen, md_sections, md_tables, cell, tabla)
        R_["cambios_b"].write_text(bloque, encoding="utf-8")
        nobj = len(cv.comparar_objetos(ant, nue, md_sections, md_tables))
        print(f"Bloque de cambios escrito: {R_['cambios_b'].name} ({nobj} objetos con cambios). Se agrega a «{R_['cambios'].name}» al registrar.")
    elif args.cmd == "pendientes":
        md = args.markdown.read_text(encoding="utf-8")
        correo, rol = _revisor(args, md)
        sec, n = "?", 0
        for k, line in enumerate(md.splitlines(), 1):
            m = re.match(r"^#{1,3} (.+)$", line)
            if m:
                sec = m.group(1)[:50]
            for x in IA.finditer(line):
                n += 1
                print(f"línea {k} · {sec} · {x.group(0)}")
        print(f"Marcadores pendientes: {n}")
        p = cv.pendientes_validacion(md, md_sections, md_tables)
        print(f"Puntos «Pendiente de validación» con el dueño: {len(p)}")
        for x in p:
            print("  " + x)
        _log_revision(args.markdown, correo, rol, "pendientes", cv.cabecera(md, "census_id"), f"{n} marcadores; {len(p)} puntos pendientes con el dueño")
    elif args.cmd == "guia-validacion":
        md = args.markdown.read_text(encoding="utf-8")
        correo, rol = _revisor(args, md)
        fx = fichas_validacion(md)
        print(f"Puntos por validar: {len(fx)} · orden: prioridad Alta, reglas inferidas, Media, Baja (R59).")
        print(f"Quien responde: {correo} ({rol}). Presente un punto a la vez con la plantilla de la guía de Kiro.\n")
        for n_, f in enumerate(fx, 1):
            print(f"=== Punto {n_} de {len(fx)} · {f['ID']} (sección {f['Sección']}, línea {f['Línea']}) · {f['Tipo']} · {f['Categoría']} · prioridad {f['Prioridad']}")
            for k in ("Qué se encontró", "Dónde", "Evidencia", "Qué depende de esto", "Impacto", "Qué hay que confirmar"):
                print(f"  {k}: {f[k]}")
            print()
        _log_revision(args.markdown, correo, rol, "guia-validacion", cv.cabecera(md, "census_id"), f"{len(fx)} puntos por presentar")
    elif args.cmd == "validar":
        md = args.markdown.read_text(encoding="utf-8")
        correo, rol = _revisor(args, md)
        err, warn, _ = validate(md, args.pbip)
        _log_revision(args.markdown, correo, rol, "validar" + (" --pbip" if args.pbip else ""), cv.cabecera(md, "census_id"),
                      f"{len(err)} errores, {len(warn)} advertencias")
        report(err, warn)
        sys.exit(1 if err else 0)
    elif args.cmd == "registrar":
        md = args.markdown.read_text(encoding="utf-8")
        err, warn, head = validate(md, args.pbip)
        R_ = _rutas(args.markdown)
        es_borrador = args.markdown.resolve() == R_["borrador"].resolve()
        if es_borrador and not R_["cambios_b"].exists():
            err.append("Falta el bloque de cambios: ejecute `censo.py comparar` antes de registrar (R52).")
        if es_borrador and R_["cambios_b"].exists() and \
                not R_["cambios_b"].read_text(encoding="utf-8").startswith(f"## {(head['census_id'] or '').strip()} ·"):
            err.append("El bloque de cambios corresponde a otro borrador: vuelva a ejecutar `censo.py comparar` (R52).")
        if R_["historial"].exists() and f"| {(head['census_id'] or '').strip()} |" in R_["historial"].read_text(encoding="utf-8"):
            err.append(f"El census_id {head['census_id']} ya está registrado; una ejecución se registra una sola vez (R38).")
        report(err, warn)
        if err:
            print("No se registró la ejecución (R42).")
            sys.exit(1)
        mails = re.findall(r"\*\*Correo[^*]+:\*\*\s*(\S+)", md)
        prev = re.search(r"\| census_id del censo anterior \| ([^|]+) \|", md)
        pend = cv.pendientes_validacion(md, md_sections, md_tables)
        if es_borrador:
            vig = R_["vigente"].read_text(encoding="utf-8")
            R_["versiones"].mkdir(exist_ok=True)
            arch = R_["versiones"] / f"{R_['bi']} - censo - {cv.cabecera(vig, 'census_id')}.md"
            R_["vigente"].replace(arch)
            args.markdown.replace(R_["vigente"])
            bloque = R_["cambios_b"].read_text(encoding="utf-8")
            R_["cambios_b"].unlink()
            print(f"Censo anterior archivado en {arch}")
        else:
            bloque = cv.bloque_cambios(None, md, "Censo inicial", md_sections, md_tables, cell, tabla)
        if not R_["cambios"].exists():
            R_["cambios"].write_text(f"# Registro de cambios entre versiones — {R_['bi']}\n\nAppend-only (R52): un bloque por ejecución "
                                     "registrada, del más antiguo al más reciente. El censo vigente (`" + R_["vigente"].name + "`) muestra "
                                     "solo el estado actual; los censos anteriores están en `versiones/`.\n\n", encoding="utf-8")
        with R_["cambios"].open("a", encoding="utf-8") as fh:
            fh.write("\n" + bloque.strip() + "\n")
        _historial(R_["historial"], {
            "census_id": head["census_id"], "Fecha y hora de ejecución": head["Fecha y hora de ejecución"], "Tipo": head["Tipo de CENSO"],
            "Versión analizada": cv.cabecera(md, "Versión analizada") or "—", "Huella del PBIP": cv.leer_huella(md) or "—",
            "census_id anterior": prev.group(1).strip() if prev else "—", "Alcance": args.alcance,
            "Correo ejecutor": mails[0] if mails else "—", "Correo dueño": mails[1] if len(mails) > 1 else "—", "Estado": head["Estado"],
            "Pendientes de validación": len(pend), "Archivo": R_["vigente"].name, "Versión del ritual": RITUAL,
            "Validador": f"0 errores, {len(warn)} advertencias ({datetime.now().astimezone().isoformat(timespec='seconds')})",
            "Observaciones": args.observaciones})
        print(f"Ejecución registrada en {R_['historial']}; cambios en {R_['cambios'].name}; censo vigente: {R_['vigente'].name}")
    elif args.cmd == "vigencia":
        md = args.markdown.read_text(encoding="utf-8")
        correo, rol = _revisor(args, md)
        print(f"Revisa: {correo} ({rol})")
        R_ = _rutas(args.markdown)
        bi, ver, hu = R_["bi"], cv.cabecera(md, "Versión analizada"), cv.leer_huella(md)
        vers = sorted(d.name for d in args.versiones.iterdir() if (d / bi).is_dir()) if args.versiones.is_dir() else []
        motivos = []
        print(f"BI: {bi} · versión censada: {ver} · versiones guardadas: {', '.join(vers) or 'ninguna'}")
        if not vers:
            motivos.append(f"No se encontró {bi} en {args.versiones}.")
        elif vers[-1] != ver:
            motivos.append(f"Hay una versión más reciente sin censar: {vers[-1]} (R53).")
        if not hu:
            motivos.append("El censo no tiene huella del PBIP (anterior a v2.3); no se puede confirmar que corresponde al tablero guardado.")
        elif ver in vers and cv.huella(args.versiones / ver / bi)[0] != hu:
            motivos.append(f"El PBIP de {ver} cambió después del censo (huella distinta) (R53).")
        if R_["borrador"].exists():
            motivos.append(f"Hay un borrador sin cerrar: {R_['borrador'].name}.")
        print("Vigencia: " + ("VIGENTE" if not motivos else "DESACTUALIZADO"))
        estado = cv.cabecera(md, "Estado")
        pend = cv.pendientes_validacion(md, md_sections, md_tables)
        if estado != "Completado y validado":
            motivos.append(f"Estado del censo: «{estado}»; el DLC exige «Completado y validado» (R56).")
        if pend:
            motivos.append(f"{len(pend)} puntos «Pendiente de validación» con el dueño (R56):")
        print("Aptitud para el DLC de modificación o depuración: " + ("APTO" if not motivos else "NO APTO"))
        vig_ = "VIGENTE" if not any(("versión más reciente" in x or "huella" in x or "borrador" in x) for x in motivos) else "DESACTUALIZADO"
        _log_revision(args.markdown, correo, rol, "vigencia", cv.cabecera(md, "census_id"), f"{vig_}; {'APTO' if not motivos else 'NO APTO'}")
        for x in motivos:
            print("  - " + x)
        for x in pend:
            print("      " + x)
        sys.exit(0 if not motivos else 1)
    elif args.cmd == "inventario":
        inv = read_pbip(args.pbip)
        args.salida_json.write_text(json.dumps(inv, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
        print(f"Inventario escrito en {args.salida_json}")


if __name__ == "__main__":
    main()
