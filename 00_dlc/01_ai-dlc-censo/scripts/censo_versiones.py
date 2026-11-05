"""Versiones del CENSO: huella del PBIP, comparación entre censos, traslado de validaciones, cierre y vigencia.

Ritual AI-DLC CENSO v2.3. Solo lectura sobre el PBIP. Usado por censo.py.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

NATIVO = re.compile(r"^([0-9a-f]{20}|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})\b")
SECC_OBJETOS = {3: "Fuente", 4: "Consulta M", 5: "Tabla o relación", 6: "Columna", 7: "Medida", 8: "Página", 9: "Visual",
                11: "Filtro, segmentación o interacción", 12: "Bookmark o botón", 13: "Recurso o elemento de diseño"}
NOMBRE_COLS = ("Nombre", "Columna", "Medida", "Página", "Tabla", "Segmentación", "Bookmark", "Tipo")
PENDIENTE = "Pendiente de validación"
RESUELTOS = {"Confirmado por el dueño", "Descartado por el dueño"}


# =============================================================================================
# Huella del PBIP
# =============================================================================================
def huella(pbip: Path) -> tuple[str, int]:
    """SHA-256 de los archivos del PBIP (ruta relativa + contenido con saltos de línea normalizados).

    Excluye lo que Power BI Desktop regenera sin que el tablero cambie: carpetas `.pbi` (configuración local y caché)
    y archivos `.abf`.
    """
    h, n = hashlib.sha256(), 0
    for p in sorted(x for x in pbip.rglob("*") if x.is_file()):
        rel = p.relative_to(pbip).as_posix()
        if ".pbi" in p.relative_to(pbip).parts or p.suffix.lower() == ".abf":
            continue
        h.update(rel.encode("utf-8") + b"\0")
        h.update(p.read_bytes().replace(b"\r\n", b"\n") + b"\0")
        n += 1
    return "sha256:" + h.hexdigest(), n


def leer_huella(md: str):
    m = re.search(r"^> Huella del PBIP:\s*(sha256:[0-9a-f]{64})", md, re.M)
    return m.group(1) if m else None


def cabecera(md: str, clave: str):
    m = re.search(rf"^> {re.escape(clave)}:\s*(.+)$", md, re.M)
    return m.group(1).strip() if m else None


# =============================================================================================
# Lectura de objetos de un censo
# =============================================================================================
def _clave(hdr, fila):
    if not fila:
        return None
    m = NATIVO.match(fila[0])
    if m:
        return m.group(1)
    if hdr and hdr[0].endswith("_id") and fila[0] not in ("", "—", "Total"):
        return fila[0]
    return None


def _nombre(hdr, fila):
    for c in NOMBRE_COLS:
        if c in hdr and hdr.index(c) < len(fila):
            v = fila[hdr.index(c)]
            if v and v != "—":
                return v.split(" · ")[-1] if NATIVO.match(v) else v
    if " · " in fila[0]:
        return fila[0].split(" · ", 1)[1]
    return "—"


def objetos(md: str, md_sections, md_tables):
    """{id: {"tipo", "nombre", "filas": {(sección, encabezado): [filas]}}} + bloques de código por nombre."""
    secs = md_sections(md)
    obj, codigo = {}, {}
    for n in SECC_OBJETOS:
        if n not in secs:
            continue
        lines = secs[n][1]
        for hdr, rows in md_tables(lines):
            for r in rows:
                k = _clave(hdr, r)
                if not k:
                    continue
                o = obj.setdefault(k, {"tipo": SECC_OBJETOS[n], "nombre": "—", "filas": {}})
                if o["nombre"] == "—":
                    o["nombre"] = _nombre(hdr, r)
                o["filas"].setdefault((n, tuple(hdr)), []).append(r)
        tit, dentro, nombre, buf = f"Sección {n}", False, "", []
        for line in lines + ["## fin"]:
            if line.startswith("#") and not dentro:
                tit = line.lstrip("# ").strip()
                continue
            if line.startswith("```"):
                if dentro:
                    codigo[(n, tit, nombre)] = "\n".join(buf).strip()
                dentro, nombre, buf = not dentro, "", []
                continue
            if dentro:
                m = re.match(r"^-- (.+)$", line)
                if m:
                    if buf and nombre:
                        codigo[(n, tit, nombre)] = "\n".join(buf).strip()
                    nombre, buf = m.group(1).strip(), []
                else:
                    buf.append(line)
    return obj, codigo


def _corto(v, n=60):
    v = str(v)
    return v if len(v) <= n else v[:n - 1] + "…"


def comparar_objetos(ant: str, nue: str, md_sections, md_tables):
    oa, ca = objetos(ant, md_sections, md_tables)
    on, cn = objetos(nue, md_sections, md_tables)
    filas = []
    for k in sorted(set(on) - set(oa), key=lambda x: (on[x]["tipo"], on[x]["nombre"])):
        filas.append(["Agregado", on[k]["tipo"], f"{k} · {on[k]['nombre']}", ", ".join(sorted({str(s) for s, _ in on[k]["filas"]})), "—"])
    for k in sorted(set(oa) - set(on), key=lambda x: (oa[x]["tipo"], oa[x]["nombre"])):
        filas.append(["Eliminado", oa[k]["tipo"], f"{k} · {oa[k]['nombre']}", ", ".join(sorted({str(s) for s, _ in oa[k]["filas"]})), "—"])
    for k in sorted(set(oa) & set(on), key=lambda x: (on[x]["tipo"], on[x]["nombre"])):
        det, secs = [], set()
        for clave in sorted(set(oa[k]["filas"]) | set(on[k]["filas"]), key=str):
            a_, n_ = oa[k]["filas"].get(clave, []), on[k]["filas"].get(clave, [])
            if sorted(a_) == sorted(n_):
                continue
            secs.add(str(clave[0]))
            hdr = list(clave[1])
            if len(a_) == 1 and len(n_) == 1:
                det += [f"{hdr[i]}: {_corto(x)} → {_corto(y)}" for i, (x, y) in enumerate(zip(a_[0], n_[0])) if x != y and i < len(hdr)]
            else:
                det.append(f"filas de la tabla «{hdr[1] if len(hdr) > 1 else hdr[0]}…»: antes {len(a_)}, ahora {len(n_)}")
        if det:
            filas.append(["Modificado", on[k]["tipo"], f"{k} · {on[k]['nombre']}", ", ".join(sorted(secs)), "; ".join(det)])
    for k in sorted(set(ca) | set(cn), key=str):
        if ca.get(k) != cn.get(k):
            cambio = "Agregado" if k not in ca else "Eliminado" if k not in cn else "Modificado"
            filas.append([cambio, "Expresión (M o DAX)", k[2] or k[1], str(k[0]), "Código distinto" if cambio == "Modificado" else "—"])
    return filas


def comparar_validaciones(ant: str, nue: str, md_sections, md_tables):
    """Cambios de estado de validación en las secciones 14 y 16 (por ID de fila)."""
    out = []
    for n, idc, estc in ((14, "rule_id", "Validación del dueño"), (16, "ID", "Estado")):
        def leer(md):
            s = md_sections(md)
            res = {}
            for hdr, rows in md_tables(s.get(n, ("", []))[1]):
                if idc in hdr and estc in hdr:
                    for r in rows:
                        res[r[hdr.index(idc)]] = (r[hdr.index(estc)], r[hdr.index("Respuesta del dueño")] if "Respuesta del dueño" in hdr else "—")
            return res
        a_, b_ = leer(ant), leer(nue)
        for k in sorted(b_):
            if k in a_ and a_[k][0] != b_[k][0]:
                out.append([k, str(n), f"{a_[k][0]} → {b_[k][0]}", b_[k][1]])
    return out


# =============================================================================================
# Traslado de validaciones y contenido de la IA del censo anterior al borrador
# =============================================================================================
def _reemplazar_tabla(md: str, hdr, filas_nuevas, cell):
    lines = md.split("\n")
    cab = "| " + " | ".join(hdr) + " |"
    i = lines.index(cab)
    j = i + 2
    while j < len(lines) and lines[j].startswith("|"):
        j += 1
    lines[i + 2:j] = ["| " + " | ".join(cell(x) for x in r) + " |" for r in filas_nuevas]
    return "\n".join(lines)


def trasladar(ant: str, nue: str, md_sections, md_tables, cell, ids_validos):
    """Copia al borrador lo que el censo anterior ya resolvió y sigue aplicando. Devuelve (md, informe)."""
    inf = []
    sa, sn = md_sections(ant), md_sections(nue)
    # 14: reglas generadas por el script (misma regla e implementación) y reglas agregadas por la IA
    ta = [t for t in md_tables(sa.get(14, ("", []))[1]) if "rule_id" in t[0]]
    tn = [t for t in md_tables(sn.get(14, ("", []))[1]) if "rule_id" in t[0]]
    if ta and tn:
        (ha, ra), (hn, rn) = ta[0], tn[0]
        ia = {(r[1], r[2]): r for r in ra}
        claves_n = {(r[1], r[2]) for r in rn}
        copiar = [c for c in ("Interpretación funcional", "Certeza", "Validación del dueño", "Respuesta del dueño") if c in ha and c in hn]
        n_cop = 0
        for r in rn:
            old = ia.get((r[1], r[2]))
            if old:
                for c in copiar:
                    r[hn.index(c)] = old[ha.index(c)]
                n_cop += 1
        extra = [r for r in ra if (r[1], r[2]) not in claves_n and not re.match(r"^(Filtro de|Columna calculada)", r[1])]
        base = len(rn)
        for i, r in enumerate(extra, 1):
            nr = ["—"] * len(hn)
            for c in hn:
                if c in ha:
                    nr[hn.index(c)] = r[ha.index(c)]
            nr[0] = f"RN{base + i:02d}"
            rn.append(nr)
        nue = _reemplazar_tabla(nue, hn, rn, cell)
        inf.append(f"Sección 14: {n_cop} reglas con interpretación y validación trasladadas; {len(extra)} reglas de conjunto de la IA "
                   "copiadas al final (revisar que sigan aplicando).")
    # 16: filas del script (mismo tipo, categoría y descripción) y filas de la IA
    sn = md_sections(nue)
    ta = [t for t in md_tables(sa.get(16, ("", []))[1]) if "Punto de revisión" in t[0]]
    tn = [t for t in md_tables(sn.get(16, ("", []))[1]) if "Punto de revisión" in t[0]]
    if ta and tn:
        (ha, ra), (hn, rn) = ta[0], tn[0]
        key = lambda h, r: (r[h.index("Tipo")], r[h.index("Categoría")], r[h.index("Descripción concreta")])  # noqa: E731
        ia = {key(ha, r): r for r in ra if re.match(r"^[HV]-A\d+$", r[0])}
        copiar = [c for c in ("Certeza", "Impacto", "Prioridad", "Estado", "Respuesta del dueño") if c in ha and c in hn]
        n_cop = 0
        for r in rn:
            old = ia.get(key(hn, r))
            if old:
                for c in copiar:
                    r[hn.index(c)] = old[ha.index(c)]
                n_cop += 1
        extra, reabiertas = [], []
        for r in ra:
            if re.match(r"^[HV]-A\d+$", r[0]):
                continue
            nr = ["—"] * len(hn)
            for c in hn:
                if c in ha:
                    nr[hn.index(c)] = r[ha.index(c)]
            citados = {x for c in r for x in re.findall(r"\b[0-9a-f]{20}\b|\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", c)}
            if citados - ids_validos and nr[hn.index("Estado")] in RESUELTOS:
                nr[hn.index("Estado")] = PENDIENTE
                reabiertas.append(r[0])
            extra.append(nr)
        rn += extra
        nue = _reemplazar_tabla(nue, hn, rn, cell)
        inf.append(f"Sección 16: {n_cop} filas del script con estado y respuesta trasladados; {len(extra)} filas de la IA copiadas"
                   + (f"; reabiertas por citar objetos que ya no existen: {', '.join(reabiertas)}" if reabiertas else "") + ".")
    return nue, inf


def guia_marcadores(ant: str, nue: str, ia_re):
    """Para cada marcador del borrador, el rango de líneas del censo anterior bajo el mismo título (para reutilizar texto)."""
    def titulos(md):
        res, cur, ini = [], None, 0
        lines = md.split("\n")
        for i, l in enumerate(lines, 1):
            if l.startswith("#"):
                if cur:
                    res.append((cur, ini, i - 1))
                cur, ini = l.lstrip("# ").strip(), i
        if cur:
            res.append((cur, ini, len(lines)))
        return res
    ta = {t: (a, b) for t, a, b in titulos(ant)}
    out, cur = [], None
    for i, l in enumerate(nue.split("\n"), 1):
        if l.startswith("#"):
            cur = l.lstrip("# ").strip()
        if ia_re.search(l) and cur in ta:
            out.append(f"línea {i} ({cur}): texto anterior en las líneas {ta[cur][0]}–{ta[cur][1]} del censo vigente")
    return out


# =============================================================================================
# Bloque del registro de cambios
# =============================================================================================
def bloque_cambios(ant: str | None, nue: str, origen: str, md_sections, md_tables, cell, tabla):
    cid, ver, tipo = cabecera(nue, "census_id"), cabecera(nue, "Versión analizada"), cabecera(nue, "Tipo de CENSO")
    fecha = cabecera(nue, "Fecha y hora de ejecución")
    L = [f"## {cid} · {tipo} · versión {ver}\n"]
    if ant is None:
        L.append(f"- Fecha: {fecha}\n- Origen: {origen}\n- Huella del PBIP: {leer_huella(nue) or '—'}\n\n"
                 "Censo inicial: no hay versión anterior con la cual comparar.\n")
        return "\n".join(L)
    cida, vera = cabecera(ant, "census_id"), cabecera(ant, "Versión analizada")
    obj = comparar_objetos(ant, nue, md_sections, md_tables)
    val = comparar_validaciones(ant, nue, md_sections, md_tables)
    L.append(f"- Fecha: {fecha}\n- Censo anterior: {cida} · versión {vera}\n- Origen del cambio: {origen}\n"
             f"- Huella del PBIP: {leer_huella(ant) or '—'} → {leer_huella(nue) or '—'}\n")
    res = {}
    for f in obj:
        res.setdefault(f[1], [0, 0, 0])[["Agregado", "Eliminado", "Modificado"].index(f[0])] += 1
    L.append("### Cambios en el tablero\n")
    if obj:
        L.append(tabla(["Tipo de objeto", "Agregados", "Eliminados", "Modificados"], [[k] + v for k, v in sorted(res.items())],
                       num=("Agregados", "Eliminados", "Modificados")))
        L.append(tabla(["Cambio", "Tipo de objeto", "ID · nombre", "Secciones", "Detalle"], obj))
    else:
        if leer_huella(ant) and leer_huella(ant) != leer_huella(nue):
            L.append("Sin cambios en lo que el censo inventaría, aunque la huella del PBIP cambió: hubo cambios en archivos u opciones "
                     "que el censo no detalla (por ejemplo, configuración del reporte). Revisar con quien guardó la versión.\n")
        else:
            L.append("Sin cambios en el tablero: el inventario y las expresiones son iguales a los del censo anterior.\n")
    L.append("### Cambios en la validación del dueño\n")
    L.append(tabla(["ID", "Sección", "Estado", "Respuesta del dueño"], val) if val else "Sin cambios de estado.\n")
    if obj and origen.strip().lower() in ("no informado", "—", ""):
        L.append("> **Alerta (R52):** el tablero cambió y no se informó el origen del cambio (DLC de modificación o de depuración).\n")
    return "\n".join(L)


# =============================================================================================
# Vigencia y aptitud para el DLC
# =============================================================================================
def pendientes_validacion(md: str, md_sections, md_tables):
    out = []
    s = md_sections(md)
    for hdr, rows in md_tables(s.get(14, ("", []))[1]):
        if "rule_id" in hdr and "Validación del dueño" in hdr:
            out += [f"14 · {r[0]} · {r[1]}" for r in rows if r[hdr.index("Validación del dueño")] == PENDIENTE]
    for hdr, rows in md_tables(s.get(16, ("", []))[1]):
        if "Punto de revisión" in hdr:
            out += [f"16 · {r[0]} · {r[hdr.index('Punto de revisión')]}" for r in rows if r[hdr.index("Estado")] == PENDIENTE]
    return out
