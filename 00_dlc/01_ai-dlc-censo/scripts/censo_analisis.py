"""Análisis de dependencias y clasificación de uso a partir del inventario PBIP. Ritual AI-DLC CENSO v2.1."""
from __future__ import annotations

from collections import Counter, defaultdict

from censo_lectura import NO_USE_OPS, dax_refs, m_steps

DECORATIVOS = {"image", "shape", "basicShape", "textbox", "visualGroup", "pageNavigator", "bookmarkNavigator", "—"}
BOTONES = {"actionButton"}
TARJETAS = {"card", "multiRowCard", "kpi", "gauge", "cardVisual"}
TIPO_LEGIBLE = {"card": "Tarjeta", "multiRowCard": "Tarjeta de varias filas", "cardVisual": "Tarjeta", "kpi": "KPI", "gauge": "Medidor",
                "slicer": "Segmentación", "advancedSlicerVisual": "Segmentación", "image": "Imagen", "shape": "Forma", "basicShape": "Forma",
                "textbox": "Cuadro de texto", "actionButton": "Botón", "tableEx": "Tabla", "pivotTable": "Matriz",
                "pieChart": "Gráfico circular", "donutChart": "Gráfico de anillos", "lineClusteredColumnComboChart": "Gráfico combinado",
                "lineStackedColumnComboChart": "Gráfico combinado", "barChart": "Gráfico de barras", "clusteredBarChart": "Gráfico de barras",
                "columnChart": "Gráfico de columnas", "clusteredColumnChart": "Gráfico de columnas", "lineChart": "Gráfico de líneas",
                "areaChart": "Gráfico de áreas", "treemap": "Mapa de árbol", "map": "Mapa", "filledMap": "Mapa coroplético",
                "visualGroup": "Grupo", "pageNavigator": "Navegador de páginas", "bookmarkNavigator": "Navegador de marcadores",
                "scatterChart": "Gráfico de dispersión", "waterfallChart": "Cascada", "funnel": "Embudo"}


def visual_name(v):
    """Nombre legible para identificar un visual en Power BI (panel Selección) junto a su ID."""
    if v.get("titulo"):
        return str(v["titulo"]).strip()
    if v.get("texto"):
        t = str(v["texto"]).strip()
        return (t[:60] + " [texto recortado]") if len(t) > 60 else t
    tipo = TIPO_LEGIBLE.get(v.get("tipo"), v.get("tipo") or "Visual")
    if v.get("bindings"):
        b = v["bindings"][0]
        campo = b["campo"] if b.get("tabla") is None else f"{b['tabla']}[{b['campo']}]"
        alias = v.get("encabezado") or b.get("native")
        if alias and alias != b["campo"]:
            return f"{tipo}: {alias} ({campo})"
        return f"{tipo}: {campo}"
    if v.get("recurso"):
        return f"{tipo}: {v['recurso']}"
    return f"{tipo} sin título"


def analyze(inv: dict) -> dict:
    tablas = {t["tabla"]: t for t in inv.get("tablas", [])}
    cols = {(t["tabla"], c["nombre"]): c for t in tablas.values() for c in t["columnas"]}
    meas = {(t["tabla"], m["nombre"]): m for t in tablas.values() for m in t["medidas"]}
    meas_by_name = defaultdict(list)
    for (t, m) in meas:
        meas_by_name[m].append(t)
    hier_levels = {}
    for t in tablas.values():
        for h in t["jerarquias"]:
            for lv, col in h["niveles"]:
                hier_levels[(t["tabla"], f"{h['nombre']}.{lv}")] = col

    def resolve_report(ent, prop):
        if (ent, prop) in cols:
            return ("col", ent, prop)
        if (ent, prop) in meas:
            return ("measure", ent, prop)
        if (ent, prop) in hier_levels:
            return ("col", ent, hier_levels[(ent, prop)])
        return ("rota", ent, prop)

    # ---------------------------------------------------------------- objetos DAX y sus referencias
    dax_objs = []
    for (t, m), mm in meas.items():
        dax_objs.append(("measure", t, m, mm["expr"]))
    for (t, c), cc in cols.items():
        if cc["calculada"]:
            dax_objs.append(("col", t, c, cc["expr"]))
    for t in tablas.values():
        for p in t["particiones"]:
            if p["tipo"].startswith("calculated"):
                dax_objs.append(("table", t["tabla"], t["tabla"], p["source"]))
    for r in inv.get("roles", []):
        for tbl, expr in r["filtros"]:
            dax_objs.append(("rls", tbl, r["rol"], expr))

    refs_of = {}
    rota_dax = []
    for kind, host, name, expr in dax_objs:
        out = []
        for tbl, ref in dax_refs(expr):
            if tbl:
                if (tbl, ref) in meas and (tbl, ref) not in cols:
                    out.append(("measure", tbl, ref))
                elif (tbl, ref) in cols:
                    out.append(("col", tbl, ref))
                else:
                    out.append(("rota", tbl, ref))
                    rota_dax.append((kind, host, name, f"{tbl}[{ref}]"))
            else:
                if ref in meas_by_name:
                    out.append(("measure", meas_by_name[ref][0], ref))
                elif (host, ref) in cols:
                    out.append(("col", host, ref))
                else:
                    out.append(("indet", host, ref))
        dedup = []
        for o in out:
            if o not in dedup and not (o[0] == kind and o[1] == host and o[2] == name):
                dedup.append(o)
        refs_of[(kind, host, name)] = dedup

    # ---------------------------------------------------------------- usos desde el reporte
    use = defaultdict(Counter)  # (kind, t, name) -> Counter(clase)
    broken_bindings = []
    orphan_formats = []
    visual_info = {}
    for v in inv.get("visuales", []):
        is_slicer = (v["tipo"] or "").lower().startswith("slicer")
        rota = False
        for b in v["bindings"]:
            if b["tabla"] is None:  # cálculo visual o expresión: se validan sus referencias internas
                rs = [resolve_report(e, p) for e, p in b.get("internas", [])]
                bad = [r for r in rs if r[0] == "rota"]
                b["estado_ref"] = "Rota" if bad else "Válida"
                for r in rs:
                    if r[0] != "rota":
                        use[(r[0], r[1], r[2])]["F" if is_slicer else "V"] += 1
                if bad:
                    rota = True
                    broken_bindings.append((v, {"rol": b["rol"], "tabla": bad[0][1], "campo": bad[0][2], "agregacion": "—"}))
                continue
            r = resolve_report(b["tabla"], b["campo"])
            b["estado_ref"] = "Rota" if r[0] == "rota" else "Válida"
            if r[0] == "rota":
                rota = True
                broken_bindings.append((v, b))
            else:
                use[(r[0], r[1], r[2])]["F" if is_slicer else "V"] += 1
        v["otros_ref"] = []
        for kind, ent, prop, agg in v["otros_campos"]:
            r = resolve_report(ent, prop)
            # Una regla de formato (colores por categoría, formato condicional, título dinámico) que apunta a una entidad
            # inexistente no impide que el visual se dibuje: es "formato huérfano", no una referencia rota de datos.
            v["otros_ref"].append((kind, ent, prop, agg, "Formato huérfano" if r[0] == "rota" else "Válida"))
            if r[0] == "rota":
                orphan_formats.append((v, ent, prop))
            else:
                use[(r[0], r[1], r[2])]["V"] += 1
        acc = [a for a in v["acciones"] if a.get("type")]
        if v["tipo"] in BOTONES or acc:
            clase = "Botón/acción"
        elif rota:
            clase = "Referencia rota"
        elif v["bindings"]:
            clase = "Con binding válido"
        else:
            clase = "Decorativo"
        visual_info[(v["page_id"], v["visual_id"])] = {"clase": clase, "rota": rota, "nombre": visual_name(v),
                                                       "formato_huerfano": any(x[4] == "Formato huérfano" for x in v["otros_ref"])}
    for f in inv.get("filtros", []):
        if f["tabla"] in ("—", None):
            continue
        r = resolve_report(f["tabla"], f["campo"])
        f["estado_ref"] = "Rota" if r[0] == "rota" else "Válida"
        if r[0] != "rota":
            use[r]["F"] += 1
    for b in inv.get("bookmarks", []):
        for kind, ent, prop, agg in b["campos"]:
            r = resolve_report(ent, prop)
            if r[0] != "rota":
                use[r]["BK"] += 1
    # ---------------------------------------------------------------- modelo
    for rel in inv.get("relaciones", []):
        use[("col", rel["tabla_desde"], rel["columna_desde"])]["M"] += 1
        use[("col", rel["tabla_hacia"], rel["columna_hacia"])]["M"] += 1
    for (t, c), cc in cols.items():
        if cc.get("sort_by"):
            use[("col", t, cc["sort_by"].strip("'"))]["M"] += 1
    for (t, _), col in hier_levels.items():
        if col:
            use[("col", t, col.strip("'"))]["M"] += 1
    for key, rl in refs_of.items():
        kind = key[0]
        for r in rl:
            if r[0] in ("col", "measure"):
                use[r]["SEC" if kind == "rls" else "D"] += 1

    # ---------------------------------------------------------------- Power Query
    consultas = []
    native_sql = []
    origin_name = {}
    for t in tablas.values():
        for p in t["particiones"]:
            if not p["tipo"].startswith("m") or not p["source"]:
                continue
            steps = m_steps(p["source"])
            consultas.append({"tabla": t["tabla"], "particion": p["nombre"], "modo": p["modo"], "pasos": steps,
                              "codigo": p["source"], "ruta": t["ruta"]})
            alias_now = {}
            for st in steps:
                for a, b in st["renombres"]:
                    alias_now[b] = alias_now.get(a, a)
                if st["op"] == "Consulta nativa" or "Query=" in st["codigo"].replace(" ", ""):
                    native_sql.append((t["tabla"], st["codigo"]))
            for (tt, c), cc in cols.items():
                if tt != t["tabla"] or cc["calculada"]:
                    continue
                src = cc.get("source_column") or c
                origin_name[(tt, c)] = alias_now.get(src, src)
                names = {src, alias_now.get(src, src), c}
                n = sum(1 for st in steps if st["op"] not in NO_USE_OPS and not st["op"].startswith("Origen")
                        and names & set(st["afecta"]))
                use[("col", tt, c)]["PQ"] += n
    tables_with_m = {q["tabla"] for q in consultas}
    has_roles = bool(inv.get("roles"))

    # ---------------------------------------------------------------- consumo transitivo
    consumed = set()
    for (kind, t, n), cnt in use.items():
        if kind in ("col", "measure") and (cnt["V"] + cnt["F"] + cnt["BK"] > 0 or (kind == "col" and cnt["M"] > 0)):
            consumed.add((kind, t, n))
    changed = True
    while changed:
        changed = False
        for (kind, host, name), rl in refs_of.items():
            if kind in ("measure", "col") and (kind, host, name) in consumed or kind in ("rls", "table"):
                for r in rl:
                    if r[0] in ("col", "measure") and r not in consumed:
                        consumed.add(r)
                        changed = True
    consumers = defaultdict(list)
    for (kind, host, name), rl in refs_of.items():
        for r in rl:
            consumers[r].append((kind, host, name))

    # ---------------------------------------------------------------- clasificación de columnas
    col_rows = {}
    for (t, c), cc in cols.items():
        u = use[("col", t, c)]
        k = {"V": u["V"], "F": u["F"], "D": u["D"], "M": u["M"], "BK": u["BK"]}
        k["PQ"] = "NA" if cc["calculada"] or t not in tables_with_m else u["PQ"]
        if native_sql:
            src = origin_name.get((t, c), c)
            k["SQL"] = sum(1 for _, sql in native_sql if src.lower() in sql.lower())
        else:
            k["SQL"] = "NA"
        k["SEC"] = u["SEC"] if has_roles else "NA"
        nota = ""
        directo = u["V"] + u["F"] + u["BK"] > 0
        via_dax = [x for x in consumers[("col", t, c)] if x in consumed and x[0] in ("measure", "col")]
        tecnico = u["M"] > 0 or (isinstance(k["PQ"], int) and k["PQ"] > 0) or (isinstance(k["SEC"], int) and k["SEC"] > 0)
        if directo or via_dax:
            estado = "En uso"
            if not directo:
                nota = "Uso indirecto vía " + ", ".join(sorted({x[2] for x in via_dax}))
        elif tecnico:
            estado = "Uso técnico"
        elif u["D"]:
            estado = "Uso desconocido"
            nota = "Solo la referencian objetos DAX sin consumo: " + ", ".join(sorted({x[2] for x in consumers[("col", t, c)]}))
        else:
            estado = "Sin uso interno identificado"
        col_rows[(t, c)] = {"clases": k, "estado": estado, "nota": nota, "origen": origin_name.get((t, c), "—")}

    # ---------------------------------------------------------------- clasificación de medidas
    norm = defaultdict(list)
    for (t, m), mm in meas.items():
        if mm["expr"].strip():
            norm["".join(mm["expr"].split()).lower()].append(m)
    meas_rows = {}
    for (t, m), mm in meas.items():
        u = use[("measure", t, m)]
        notas = []
        if not mm["expr"].strip():
            notas.append("Sin expresión")
        dups = [x for x in norm.get("".join(mm["expr"].split()).lower(), []) if x != m]
        if dups:
            notas.append("Misma expresión que " + ", ".join(dups))
        if ("measure", t, m) in consumed:
            estado = "En uso"
        elif u["D"]:
            estado = "Uso desconocido"
            notas.append("Solo la referencian medidas sin consumo: " + ", ".join(sorted({x[2] for x in consumers[("measure", t, m)]})))
        else:
            estado = "Sin uso interno identificado"
        usa = [f"{r[2]}" if r[0] == "measure" else f"{r[1]}[{r[2]}]" for r in refs_of.get(("measure", t, m), []) if r[0] != "indet"]
        meas_rows[(t, m)] = {"V": u["V"], "F": u["F"], "BK": u["BK"], "D": u["D"], "estado": estado, "nota": "; ".join(notas),
                             "usa": usa}

    # ---------------------------------------------------------------- visuales, bookmarks, recursos
    shown = set()
    invoked = defaultdict(list)
    for v in inv.get("visuales", []):
        for a in v["acciones"]:
            if a.get("bookmark"):
                invoked[a["bookmark"]].append(v["visual_id"])
        if v["tipo"] == "bookmarkNavigator":
            for b in inv.get("bookmarks", []):
                invoked[b["bookmark_id"]].append(v["visual_id"])
    for b in inv.get("bookmarks", []):
        for (sec, mode, exists), vids in b["estados"].items():
            if mode != "hidden":
                for vid in vids:
                    shown.add((sec, vid))
    for v in inv.get("visuales", []):
        vi = visual_info[(v["page_id"], v["visual_id"])]
        if vi["rota"]:
            vi["estado"] = "Referencia rota"
        elif v["oculto"] and (v["page_id"], v["visual_id"]) not in shown:
            vi["estado"] = "Uso desconocido"
        else:
            vi["estado"] = "En uso"
    page_ids = {p["page_id"] for p in inv.get("paginas", [])}
    by_vid = {}
    for v in inv.get("visuales", []):
        by_vid.setdefault(v["visual_id"], v)
    for b in inv.get("bookmarks", []):
        b["invocado_por"] = invoked.get(b["bookmark_id"], [])
        states = {}
        for (sec, mode, exists), vids in b["estados"].items():
            for vid in vids:
                states[vid] = "Oculta" if mode == "hidden" else "Muestra"
        aplica_solo = str(b.get("solo_targets", "")).lower() == "true" and b["targets"]
        detalle = []
        for t in b["targets"]:
            vv = by_vid.get(t)
            info = visual_info.get((vv["page_id"], t)) if vv else None
            detalle.append({"id": t, "existe": vv is not None, "nombre": info["nombre"] if info else "no existe en el PBIP",
                            "funciona": (not info["rota"]) if info else False, "efecto": states.get(t, "Sin estado guardado")})
        b["targets_detalle"] = detalle
        b["aplica_solo_targets"] = bool(aplica_solo)
        aplicados = {d["id"] for d in detalle} if aplica_solo else set(states)
        b["estados_sin_efecto"] = sorted(v for v in states if v not in aplicados)
        b["estados_guardados"] = states
        b["estados_aplicados"] = {vid: st for vid, st in states.items() if vid in aplicados}
        funcionales = [d for d in detalle if d["existe"] and d["funciona"]]
        if not b["seccion_existe"]:
            b["estado"] = "Referencia rota"
            b["motivo"] = "La página del bookmark no existe"
        elif detalle and not funcionales:
            b["estado"] = "Referencia rota"
            b["motivo"] = "Todos sus targets están rotos o no existen"
        elif b["invocado_por"]:
            b["estado"] = "En uso"
            b["motivo"] = "Lo invoca un botón o navegador"
        else:
            b["estado"] = "Uso desconocido"
            b["motivo"] = "Ningún botón lo invoca; puede usarse desde el panel de marcadores"
    for r in inv.get("recursos", []):
        if not r.get("existe"):
            r["estado"] = "Referencia rota"
        elif r.get("usado_por"):
            r["estado"] = "En uso"
        elif str(r.get("ruta", "")).find("BaseThemes") >= 0 or (r.get("resource_id") in (inv.get("tema") or {}).values()):
            r["estado"] = "Uso técnico"
        else:
            r["estado"] = "Sin uso interno identificado"
    phantom_pages = defaultdict(lambda: {"bookmarks": [], "botones": []})
    for b in inv.get("bookmarks", []):
        if b["seccion"] and not b["seccion_existe"]:
            phantom_pages[b["seccion"]]["bookmarks"].append(b["bookmark_id"])
    for v in inv.get("visuales", []):
        for a in v["acciones"]:
            dest = a.get("navigationSection") or a.get("drillthroughSection")
            if dest and dest not in page_ids:
                phantom_pages[dest]["botones"].append(v["visual_id"])
    return {"cols": cols, "meas": meas, "col_rows": col_rows, "meas_rows": meas_rows, "visual_info": visual_info,
            "consultas": consultas, "broken_bindings": broken_bindings, "orphan_formats": orphan_formats, "by_vid": by_vid, "rota_dax": rota_dax, "phantom_pages": dict(phantom_pages),
            "native_sql": native_sql, "has_roles": has_roles, "refs_of": refs_of, "use": use, "consumers": consumers}
