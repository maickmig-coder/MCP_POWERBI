"""Lectura de un proyecto PBIP (PBIR + TMDL) en modo solo lectura. Ritual AI-DLC CENSO v2.1.

No modifica ningún archivo. Usado por censo.py.
"""
from __future__ import annotations

import json
import re
import struct
import textwrap
from collections import defaultdict
from pathlib import Path

AGG = {0: "Sum", 1: "Avg", 2: "Count", 3: "Min", 4: "Max", 5: "CountNonNull", 6: "Median", 7: "StandardDeviation", 8: "Variance"}
CMP = {0: "=", 1: ">", 2: ">=", 3: "<", 4: "<="}
AUTO_DATE = ("LocalDateTable_", "DateTableTemplate_")
LONG_LITERAL = 300


# =============================================================================================
# Utilidades
# =============================================================================================
def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001
        return {"__error__": f"{type(exc).__name__}: {exc}"}


def find_all(obj, key):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == key:
                yield v
            yield from find_all(v, key)
    elif isinstance(obj, list):
        for v in obj:
            yield from find_all(v, key)


def lit(v):
    """Valor legible de un Literal PBIR ('texto', 12L, true, null, datetime'...')."""
    if isinstance(v, dict):
        for x in find_all(v, "Literal"):
            return lit(x.get("Value"))
        return None
    if not isinstance(v, str):
        return v
    s = v
    if len(s) >= 2 and s[0] == "'" and s[-1] == "'":
        return s[1:-1].replace("''", "'")
    if re.fullmatch(r"-?\d+L", s):
        return s[:-1]
    if re.fullmatch(r"-?\d+(\.\d+)?D", s):
        return s[:-1]
    return s


def obj_prop(objects, name, prop):
    """Primer literal de objects[name][*].properties[prop]."""
    for entry in (objects or {}).get(name, []) or []:
        p = (entry or {}).get("properties", {}).get(prop)
        if p is not None:
            return lit(p)
    return None


def image_size(path: Path):
    try:
        data = path.read_bytes()
    except OSError:
        return None, None
    try:
        if data[:8] == b"\x89PNG\r\n\x1a\n":
            return struct.unpack(">II", data[16:24])
        if data[:6] in (b"GIF87a", b"GIF89a"):
            return struct.unpack("<HH", data[6:10])
        if data[:2] == b"BM":
            w, h = struct.unpack("<ii", data[18:26])
            return w, abs(h)
        if data[:2] == b"\xff\xd8":
            i = 2
            while i < len(data) - 9:
                if data[i] != 0xFF:
                    i += 1
                    continue
                marker = data[i + 1]
                if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                    h, w = struct.unpack(">HH", data[i + 5:i + 9])
                    return w, h
                i += 2 + struct.unpack(">H", data[i + 2:i + 4])[0]
        if path.suffix.lower() == ".svg":
            txt = data[:4000].decode("utf-8", "ignore")
            w, h = re.search(r'\bwidth="([\d.]+)', txt), re.search(r'\bheight="([\d.]+)', txt)
            if w and h:
                return round(float(w.group(1))), round(float(h.group(1)))
            vb = re.search(r'viewBox="[\d.\-]+[\s,]+[\d.\-]+[\s,]+([\d.]+)[\s,]+([\d.]+)"', txt)
            if vb:
                return round(float(vb.group(1))), round(float(vb.group(2)))
    except struct.error:
        pass
    return None, None


# =============================================================================================
# TMDL
# =============================================================================================
KEYWORDS = ("table", "column", "measure", "hierarchy", "level", "partition", "relationship", "role", "tablePermission",
            "expression", "model", "database", "annotation", "calculationGroup", "calculationItem", "perspective",
            "culture", "variation", "extendedProperty", "dataSource", "ref", "queryGroup", "columnPermission")


def _split_name(rest: str):
    rest = rest.strip()
    if rest.startswith("'"):
        m = re.match(r"'((?:[^']|'')*)'(.*)$", rest)
        name, tail = (m.group(1).replace("''", "'"), m.group(2)) if m else (rest, "")
    else:
        m = re.match(r"([^\s=]+)(.*)$", rest)
        name, tail = (m.group(1), m.group(2)) if m else (rest, "")
    tail = tail.strip()
    return name, (tail[1:] if tail.startswith("=") else None)


def _dedent(lines):
    while lines and not lines[-1].strip():
        lines.pop()
    while lines and not lines[0].strip():
        lines.pop(0)
    return textwrap.dedent("\n".join(lines)).strip("\n")


def _read_expr(lines, i, ind, first):
    first = first.strip()
    if first.startswith("```"):
        rest = first[3:].strip()
        if rest.endswith("```") and len(rest) >= 3:
            return rest[:-3].strip(), i + 1
        body, j = ([rest] if rest else []), i + 1
        while j < len(lines) and lines[j].strip() != "```":
            body.append(lines[j])
            j += 1
        return _dedent(body), j + 1
    if first == "":
        body, j = [], i + 1
        while j < len(lines):
            line = lines[j]
            if not line.strip():
                body.append("")
                j += 1
                continue
            if len(line) - len(line.lstrip("\t")) <= ind + 1:
                break
            body.append(line)
            j += 1
        return _dedent(body), j
    return first, i + 1


def parse_tmdl(text: str) -> list[dict]:
    lines = text.splitlines()
    roots, stack, i = [], [], 0
    while i < len(lines):
        raw = lines[i]
        if not raw.strip() or raw.strip().startswith("///"):
            i += 1
            continue
        ind = len(raw) - len(raw.lstrip("\t"))
        s = raw.strip()
        while stack and stack[-1]["_ind"] >= ind:
            stack.pop()
        parent = stack[-1] if stack else None
        m = re.match(r"^(\w+)\b\s*(.*)$", s)
        if m and m.group(1) in KEYWORDS and not re.match(r"^\w+\s*:", s):
            kind, rest = m.groups()
            name, expr = _split_name(rest)
            obj = {"kind": kind, "name": name, "props": {}, "children": [], "_ind": ind, "expr": None}
            if expr is not None:
                obj["expr"], i = _read_expr(lines, i, ind, expr)
            else:
                i += 1
            (parent["children"] if parent else roots).append(obj)
            stack.append(obj)
            continue
        if parent is not None:
            bare = parent.get("_bare")
            prefix = ""
            if bare and ind > bare[0]:
                prefix = bare[1] + "."
                parent["props"].pop(bare[1], None)
            elif bare and ind <= bare[0]:
                parent["_bare"] = None
            m = re.match(r"^([A-Za-z_]\w*)\s*(:|=)\s*(.*)$", s)
            if m:
                key, sep, val = m.groups()
                if sep == "=":
                    val, i = _read_expr(lines, i, ind, val)
                    parent["props"][prefix + key] = val
                    continue
                parent["props"][prefix + key] = val.strip()
            elif re.match(r"^\w+$", s):
                parent["props"][prefix + s] = True
                if not prefix:
                    parent["_bare"] = (ind, s)
        i += 1
    return roots


def _col_ref(s: str):
    """'Tabla X'.Columna  |  Tabla.'Col Y'  ->  (tabla, columna)."""
    s = s.strip()
    if s.startswith("'"):
        m = re.match(r"'((?:[^']|'')*)'\.(.*)$", s)
        t, c = (m.group(1).replace("''", "'"), m.group(2)) if m else (s, "")
    else:
        t, _, c = s.partition(".")
    c = c.strip()
    if c.startswith("'") and c.endswith("'"):
        c = c[1:-1].replace("''", "'")
    return t, c


def read_model(sm_def: Path, root: Path) -> dict:
    model = {"tablas": [], "relaciones": [], "roles": [], "parametros": [], "propiedades": {}, "advertencias": []}
    for tf in sorted((sm_def / "tables").glob("*.tmdl")) if (sm_def / "tables").is_dir() else []:
        for t in parse_tmdl(tf.read_text(encoding="utf-8-sig")):
            if t["kind"] != "table":
                continue
            tab = {"tabla": t["name"], "table_id": t["props"].get("lineageTag"), "oculta": bool(t["props"].get("isHidden")),
                   "ruta": tf.relative_to(root).as_posix(), "auto": t["name"].startswith(AUTO_DATE),
                   "columnas": [], "medidas": [], "jerarquias": [], "particiones": []}
            for ch in t["children"]:
                p = ch["props"]
                if ch["kind"] == "column":
                    tab["columnas"].append({"nombre": ch["name"], "column_id": p.get("lineageTag"), "tipo_dato": p.get("dataType"),
                                            "calculada": ch["expr"] is not None, "expr": ch["expr"], "oculta": bool(p.get("isHidden")),
                                            "source_column": p.get("sourceColumn"), "sort_by": p.get("sortByColumn"),
                                            "formato": p.get("formatString"), "categoria": p.get("dataCategory")})
                elif ch["kind"] == "measure":
                    tab["medidas"].append({"nombre": ch["name"], "measure_id": p.get("lineageTag"), "expr": ch["expr"] or "",
                                           "formato": p.get("formatString"), "carpeta": p.get("displayFolder"),
                                           "oculta": bool(p.get("isHidden"))})
                elif ch["kind"] == "hierarchy":
                    tab["jerarquias"].append({"nombre": ch["name"], "hierarchy_id": p.get("lineageTag"),
                                              "niveles": [(lv["name"], lv["props"].get("column")) for lv in ch["children"] if lv["kind"] == "level"]})
                elif ch["kind"] == "partition":
                    tab["particiones"].append({"nombre": ch["name"], "tipo": (ch["expr"] or "").strip(), "modo": p.get("mode", "import"),
                                               "source": p.get("source", ""), "query_group": p.get("queryGroup")})
            model["tablas"].append(tab)
    rel = sm_def / "relationships.tmdl"
    if rel.exists():
        for r in parse_tmdl(rel.read_text(encoding="utf-8-sig")):
            if r["kind"] != "relationship":
                continue
            p = r["props"]
            ft, fc = _col_ref(p.get("fromColumn", ""))
            tt, tc = _col_ref(p.get("toColumn", ""))
            model["relaciones"].append({"relationship_id": r["name"], "tabla_desde": ft, "columna_desde": fc, "tabla_hacia": tt,
                                        "columna_hacia": tc, "activa": str(p.get("isActive", "true")).lower() != "false",
                                        "card_desde": p.get("fromCardinality", "many"), "card_hacia": p.get("toCardinality", "one"),
                                        "filtro": p.get("crossFilteringBehavior", "oneDirection"),
                                        "join_fecha": p.get("joinOnDateBehavior", "—"), "ruta": rel.relative_to(root).as_posix()})
    for rf in sorted((sm_def / "roles").glob("*.tmdl")) if (sm_def / "roles").is_dir() else []:
        for r in parse_tmdl(rf.read_text(encoding="utf-8-sig")):
            if r["kind"] == "role":
                model["roles"].append({"rol": r["name"], "permiso": r["props"].get("modelPermission", "—"),
                                       "filtros": [(tp["name"], tp["expr"] or "") for tp in r["children"] if tp["kind"] == "tablePermission"],
                                       "ruta": rf.relative_to(root).as_posix()})
    ex = sm_def / "expressions.tmdl"
    if ex.exists():
        for e in parse_tmdl(ex.read_text(encoding="utf-8-sig")):
            if e["kind"] == "expression":
                model["parametros"].append({"nombre": e["name"], "expr": e["expr"] or "", "ruta": ex.relative_to(root).as_posix()})
    for fname in ("model.tmdl", "database.tmdl"):
        f = sm_def / fname
        if not f.exists():
            continue
        for o in parse_tmdl(f.read_text(encoding="utf-8-sig")):
            if o["kind"] in ("model", "database"):
                for k, v in o["props"].items():
                    model["propiedades"][k] = v
                for ch in o["children"]:
                    if ch["kind"] == "annotation" and ch["name"].startswith("__PBI_TimeIntelligenceEnabled"):
                        model["propiedades"]["__PBI_TimeIntelligenceEnabled"] = (ch["expr"] or "").strip()
    return model


# =============================================================================================
# Power Query / M
# =============================================================================================
M_OPS = {
    "Table.RemoveColumns": "Eliminación de columnas", "Table.RenameColumns": "Renombrado", "Table.TransformColumnTypes": "Cambio de tipo",
    "Table.SelectRows": "Filtro de filas", "Table.TransformColumns": "Transformación de columnas", "Table.AddColumn": "Columna personalizada",
    "Table.NestedJoin": "Combinación", "Table.Join": "Combinación", "Table.ExpandTableColumn": "Expansión", "Table.Group": "Agrupación",
    "Table.Sort": "Ordenamiento", "Table.Combine": "Anexado", "Table.Pivot": "Dinamización", "Table.Unpivot": "Anulación de dinamización",
    "Table.UnpivotOtherColumns": "Anulación de dinamización", "Table.ReplaceValue": "Reemplazo de valores", "Table.Distinct": "Quitar duplicados",
    "Table.SelectColumns": "Selección de columnas", "Table.ReorderColumns": "Reordenamiento", "Table.PromoteHeaders": "Promover encabezados",
    "Table.FromRows": "Tabla embebida", "Table.Buffer": "Búfer", "Table.FillDown": "Rellenar hacia abajo", "Table.DuplicateColumn": "Duplicar columna",
    "Table.SplitColumn": "Dividir columna", "Table.CombineColumns": "Combinar columnas", "Table.FirstN": "Primeras filas",
    "Table.Skip": "Omitir filas", "Table.RemoveRowsWithErrors": "Quitar errores", "Table.ReplaceErrorValues": "Reemplazar errores",
    "Value.NativeQuery": "Consulta nativa", "#table": "Tabla literal",
}
NO_USE_OPS = {"Eliminación de columnas", "Renombrado", "Cambio de tipo", "Navegación", "Origen", "Selección de columnas", "Reordenamiento",
              "Transformación de columnas", "Reemplazo de valores", "Reemplazar errores", "Rellenar hacia abajo",
              "Búfer", "Promover encabezados", "Tabla embebida", "Tabla literal", "Expresión"}


def _m_mask(code: str):
    """Devuelve una copia del código con cadenas y comentarios reemplazados por espacios (misma longitud)."""
    out, i, n = list(code), 0, len(code)
    while i < n:
        ch = code[i]
        if ch == '"':
            j = i + 1
            while j < n:
                if code[j] == '"' and j + 1 < n and code[j + 1] == '"':
                    j += 2
                    continue
                if code[j] == '"':
                    break
                j += 1
            for k in range(i + 1, min(j, n)):
                out[k] = " "
            i = j + 1
        elif code.startswith("//", i):
            j = code.find("\n", i)
            j = n if j < 0 else j
            for k in range(i, j):
                out[k] = " "
            i = j
        elif code.startswith("/*", i):
            j = code.find("*/", i + 2)
            j = n if j < 0 else j + 2
            for k in range(i, j):
                if out[k] != "\n":
                    out[k] = " "
            i = j
        else:
            i += 1
    return "".join(out)


def m_steps(code: str) -> list[dict]:
    mask = _m_mask(code)
    m = re.search(r"\blet\b", mask)
    if not m:
        return [{"idx": 1, "paso": "(expresión)", "op": "Expresión", "codigo": code.strip(), "afecta": []}]
    depth, last_in, start = 0, None, m.end()
    for i in range(start, len(mask)):
        c = mask[i]
        if c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
        elif depth == 0 and mask.startswith("in", i) and (i == 0 or not mask[i - 1].isalnum()) and \
                (i + 2 >= len(mask) or not (mask[i + 2].isalnum() or mask[i + 2] in "_.")):
            last_in = i
    body_end = last_in if last_in is not None else len(mask)
    pieces, depth, s0 = [], 0, start
    for i in range(start, body_end):
        c = mask[i]
        if c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
        elif c == "," and depth == 0:
            pieces.append((s0, i))
            s0 = i + 1
    pieces.append((s0, body_end))
    steps = []
    for a, b in pieces:
        seg, segm = code[a:b], mask[a:b]
        if not seg.strip():
            continue
        eq = None
        for k, c in enumerate(segm):
            if c == "=" and segm[k + 1:k + 2] != ">" and segm[k - 1:k] not in ("<", ">"):
                eq = k
                break
        if eq is None:
            continue
        name = seg[:eq].strip()
        if name.startswith('#"') and name.endswith('"'):
            name = name[2:-1].replace('""', '"')
        expr = seg[eq + 1:].strip()
        steps.append({"idx": len(steps) + 1, "paso": name, "codigo": expr})
    for st in steps:
        st.update(_m_classify(st["codigo"]))
    if steps and steps[0]["op"] not in ("Origen", "Tabla embebida", "Tabla literal"):
        steps[0]["op"] = f"Origen ({steps[0]['funcion'] or 'expresión'})"
    return steps


def _strings(s):
    return [x.replace('""', '"') for x in re.findall(r'"((?:[^"]|"")*)"', s)]


def _m_classify(expr: str) -> dict:
    fm = re.match(r"\s*(#table|[A-Z][\w]*(?:\.[\w]+)+)\s*\(", expr)
    func = fm.group(1) if fm else ""
    if re.match(r"\s*[\w#\"]+\s*\{\s*\[", expr) and not func:
        op = "Navegación"
    else:
        op = M_OPS.get(func, func or "Expresión")
    if func.startswith(("Sql.", "Odbc.", "OleDb.", "AmazonAthena.", "Snowflake.", "GoogleBigQuery.", "Databricks.", "Excel.", "Csv.",
                        "Web.", "SharePoint.", "Folder.", "File.", "PostgreSQL.", "MySQL.", "Oracle.", "AnalysisServices.",
                        "PowerBI.", "Dataflows", "OData.", "AzureStorage.", "Lakehouse.", "Fabric.")):
        op = "Origen"
    afecta, renombres, tipos, eliminadas, nuevas = [], [], [], [], []
    if op == "Renombrado":
        renombres = [(a.replace('""', '"'), b.replace('""', '"')) for a, b in re.findall(r'\{\s*"((?:[^"]|"")*)"\s*,\s*"((?:[^"]|"")*)"\s*\}', expr)]
        afecta = [b for _, b in renombres]
    elif op == "Cambio de tipo":
        tipos = [(a.replace('""', '"'), t.strip()) for a, t in re.findall(r'\{\s*"((?:[^"]|"")*)"\s*,\s*([^{}]+?)\s*\}', expr)]
        afecta = [a for a, _ in tipos]
    elif op in ("Eliminación de columnas", "Selección de columnas", "Reordenamiento"):
        afecta = _strings(expr)
        if op == "Eliminación de columnas":
            eliminadas = afecta
    elif op == "Transformación de columnas":
        afecta = [a.replace('""', '"') for a in re.findall(r'\{\s*"((?:[^"]|"")*)"\s*,', expr)]
    elif op == "Columna personalizada":
        ss = _strings(expr)
        nuevas = ss[:1]
        afecta = nuevas + [r for r in re.findall(r"\[([^\]=\[]+)\]", _m_mask(expr))]
    elif op == "Navegación":
        afecta = []
    else:
        afecta = [r.strip() for r in re.findall(r"\[([^\]=\[]+)\]", _m_mask(expr))] + \
            ([a.replace('""', '"') for a in re.findall(r'\{\s*"((?:[^"]|"")*)"\s*,', expr)] if func.startswith("Table.") else [])
    seen, uniq = set(), []
    for a in afecta:
        if a and a not in seen:
            seen.add(a)
            uniq.append(a)
    nav = re.findall(r'Name\s*=\s*"((?:[^"]|"")*)"', expr) if op == "Navegación" else []
    return {"op": op, "funcion": func, "afecta": uniq, "renombres": renombres, "tipos": tipos, "eliminadas": eliminadas,
            "nuevas": nuevas, "navegacion": nav}


def elide_long_literals(code: str, ruta: str) -> str:
    def repl(m):
        s = m.group(0)
        return f'"[[literal de {len(s) - 2} caracteres omitido; ver {ruta}]]"' if len(s) > LONG_LITERAL else s
    return re.sub(r'"(?:[^"]|"")*"', repl, code)


# =============================================================================================
# DAX
# =============================================================================================
def _dax_mask(expr: str) -> str:
    s = re.sub(r'"(?:[^"]|"")*"', '""', expr)
    s = re.sub(r"/\*.*?\*/", " ", s, flags=re.S)
    s = re.sub(r"(//|--)[^\n]*", " ", s)
    return s


def dax_refs(expr: str):
    """[(tabla|None, nombre)] de las referencias entre corchetes de una expresión DAX."""
    out = []
    s = _dax_mask(expr or "")
    for m in re.finditer(r"(?:'((?:[^']|'')+)'|([A-Za-z_][\w]*))?\[([^\]]+)\]", s):
        t = (m.group(1) or "").replace("''", "'") or m.group(2)
        out.append((t, m.group(3).strip()))
    return out


# =============================================================================================
# Reporte PBIR
# =============================================================================================
def field_refs(obj):
    """[(tipo, entidad, propiedad, agregacion)] de todos los campos referenciados en un JSON PBIR."""
    alias = {}
    for frm in find_all(obj, "From"):
        for f in frm or []:
            if isinstance(f, dict) and f.get("Name") and f.get("Entity"):
                alias[f["Name"]] = f["Entity"]
    out = []

    def ent(node):
        sr = (node.get("Expression") or {}).get("SourceRef") or {}
        return sr.get("Entity") or alias.get(sr.get("Source"))

    def walk(o, agg=None):
        if isinstance(o, dict):
            for kind in ("Column", "Measure"):
                n = o.get(kind)
                if isinstance(n, dict) and "Property" in n:
                    out.append((kind, ent(n), n.get("Property"), agg))
            hl = o.get("HierarchyLevel")
            if isinstance(hl, dict):
                h = (hl.get("Expression") or {}).get("Hierarchy") or {}
                out.append(("HierarchyLevel", ent(h), f"{h.get('Hierarchy')}.{hl.get('Level')}", agg))
            a = o.get("Aggregation")
            if isinstance(a, dict):
                walk(a.get("Expression"), AGG.get(a.get("Function"), f"Función {a.get('Function')}"))
            for k, v in o.items():
                if k not in ("Aggregation",):
                    walk(v, agg if k in ("Column", "Measure") else None)
        elif isinstance(o, list):
            for v in o:
                walk(v, agg)

    walk(obj)
    seen, uniq = set(), []
    for r in out:
        if r not in seen:
            seen.add(r)
            uniq.append(r)
    return uniq


def cond_text(f: dict) -> str:
    flt = f.get("filter") or {}
    if f.get("type") == "TopN":
        tops = list(find_all(flt, "Top"))
        return f"TopN {tops[0]}" if tops else "TopN"

    def r(c):
        if not isinstance(c, dict):
            return "?"
        if "In" in c:
            vals = [lit(v) for row in c["In"].get("Values", []) for v in row]
            return "IN (" + ", ".join("null" if v in (None, "null") else str(v) for v in vals) + ")"
        if "Not" in c:
            return "NOT " + r(c["Not"].get("Expression"))
        if "Comparison" in c:
            cm = c["Comparison"]
            return f"{CMP.get(cm.get('ComparisonKind'), '?')} {lit(cm.get('Right'))}"
        for k in ("And", "Or"):
            if k in c:
                return f"({r(c[k].get('Left'))} {k.upper()} {r(c[k].get('Right'))})"
        for k in ("Contains", "StartsWith", "EndsWith"):
            if k in c:
                return f"{k} {lit(c[k].get('Right'))}"
        return json.dumps(c, ensure_ascii=False)[:120]

    wh = flt.get("Where") or []
    if not wh:
        return "Sin condición guardada"
    return " AND ".join(r(w.get("Condition")) for w in wh)


def read_report(rep: Path, root: Path) -> dict:
    d = rep / "definition"
    out = {"paginas": [], "visuales": [], "filtros": [], "interacciones": [], "bookmarks": [], "recursos": [], "tema": {},
           "metadatos": {}, "advertencias": []}
    if (rep / "definition.pbir").exists():
        pbir = load_json(rep / "definition.pbir")
        ref = (pbir.get("datasetReference") or {})
        out["metadatos"]["modelo_referenciado"] = ((ref.get("byPath") or {}).get("path")
                                                   or ("Conexión: " + json.dumps(ref.get("byConnection"), ensure_ascii=False)[:150] if ref.get("byConnection") else "—"))
        out["metadatos"]["version_pbir"] = pbir.get("version")
    if (rep / ".platform").exists():
        out["metadatos"]["report_logicalId"] = load_json(rep / ".platform").get("config", {}).get("logicalId")
    if not d.is_dir():
        out["advertencias"].append(f"{rep.name}: sin carpeta definition/ (PBIR-Legacy); inspeccionar report.json manualmente.")
        return out
    rj = load_json(d / "report.json") if (d / "report.json").exists() else {}
    tc = rj.get("themeCollection", {})
    out["tema"] = {"base": (tc.get("baseTheme") or {}).get("name"), "personalizado": (tc.get("customTheme") or {}).get("name")}
    for f in (rj.get("filterConfig") or {}).get("filters", []) or []:
        out["filtros"].append(_filter(f, "Informe", "—", "—"))
    registered = {}
    for pkg in rj.get("resourcePackages", []) or []:
        for item in pkg.get("items", []) or []:
            registered[item.get("name")] = {"resource_id": item.get("name"), "paquete": pkg.get("name"), "tipo": item.get("type"),
                                            "ruta_declarada": item.get("path"), "usado_por": []}
    pages_meta = load_json(d / "pages" / "pages.json") if (d / "pages" / "pages.json").exists() else {}
    order = pages_meta.get("pageOrder", [])
    out["metadatos"]["pagina_activa"] = pages_meta.get("activePageName")

    def mark(obj, pid, vid, uso):
        for ref in find_all(obj, "ResourcePackageItem"):
            name = lit(ref.get("ItemName")) if isinstance(ref.get("ItemName"), dict) else ref.get("ItemName")
            item = registered.setdefault(name, {"resource_id": name, "paquete": ref.get("PackageName"), "tipo": None,
                                                "ruta_declarada": name, "usado_por": [], "sin_registro": True})
            item["usado_por"].append((pid, vid, uso))

    for pdir in sorted(p for p in (d / "pages").glob("*") if p.is_dir()) if (d / "pages").is_dir() else []:
        pj = pdir / "page.json"
        if not pj.exists():
            continue
        page = load_json(pj)
        pid = page.get("name", pdir.name)
        objs = page.get("objects", {})
        bg = obj_prop(objs, "background", "color")
        binding = (page.get("pageBinding") or {}).get("type")
        vdirs = sorted(p for p in (pdir / "visuals").glob("*") if p.is_dir()) if (pdir / "visuals").is_dir() else []
        out["paginas"].append({"page_id": pid, "ruta": pj.relative_to(root).as_posix(), "pagina": page.get("displayName"),
                               "orden": order.index(pid) + 1 if pid in order else None,
                               "visibilidad": "Oculta" if page.get("visibility") == "HiddenInViewMode" else "Visible",
                               "ancho": page.get("width"), "alto": page.get("height"), "display": page.get("displayOption"),
                               "fondo": bg or "—", "tipo": binding or page.get("type") or "Normal", "total_visuales": len(vdirs)})
        mark(objs, pid, "—", "fondo de página")
        for f in (page.get("filterConfig") or {}).get("filters", []) or []:
            out["filtros"].append(_filter(f, "Página", pid, "—"))
        for it in page.get("visualInteractions", []) or []:
            out["interacciones"].append({"page_id": pid, "origen": it.get("source"), "destino": it.get("target"), "tipo": it.get("type")})
        for vdir in vdirs:
            vj = vdir / "visual.json"
            if not vj.exists():
                continue
            v = load_json(vj)
            vid = v.get("name", vdir.name)
            pos = v.get("position", {})
            vis = v.get("visual", {}) or {}
            grp = v.get("visualGroup")
            vtype = vis.get("visualType") or ("visualGroup" if grp is not None else "—")
            bindings = []
            for role, st in ((vis.get("query") or {}).get("queryState") or {}).items():
                for proj in st.get("projections", []) or []:
                    fld = proj.get("field", {}) or {}
                    top = next(iter(fld), "")
                    refs = field_refs(fld)
                    if top in ("Column", "Measure", "Aggregation", "HierarchyLevel") and refs:
                        kind, ent_, prop, agg = refs[0]
                        bindings.append({"rol": role, "tipo": kind, "tabla": ent_, "campo": prop, "agregacion": agg or "—",
                                         "native": proj.get("nativeQueryRef"), "internas": []})
                    else:
                        bindings.append({"rol": role, "tipo": f"Expresión ({top or '—'})", "tabla": None,
                                         "campo": proj.get("nativeQueryRef") or proj.get("queryRef") or top, "agregacion": "Cálculo visual",
                                         "native": proj.get("nativeQueryRef"), "internas": [(e, p) for _, e, p, _ in refs]})
            q_keys = {(b["tabla"], b["campo"]) for b in bindings}
            otros = [(k, e, p, a) for k, e, p, a in field_refs({"o": vis.get("objects"), "c": vis.get("visualContainerObjects")})
                     if (e, p) not in q_keys]
            title = obj_prop(vis.get("visualContainerObjects"), "title", "text")
            if grp is not None:
                title = grp.get("displayName")
            texts = []
            for para in find_all(vis.get("objects", {}), "paragraphs"):
                for p in para or []:
                    texts.append("".join(r.get("value", "") for r in p.get("textRuns", []) or []))
            btn_text = obj_prop(vis.get("objects"), "text", "text")
            acciones = []
            for vl in find_all(vis.get("visualContainerObjects", {}), "visualLink"):
                for e in vl or []:
                    pr = (e or {}).get("properties", {})
                    acciones.append({k: lit(pr.get(k)) for k in ("show", "type", "bookmark", "navigationSection", "drillthroughSection", "webUrl")})
            mark(v, pid, vid, vtype)
            recurso = None
            for ref in find_all(v, "ResourcePackageItem"):
                recurso = lit(ref.get("ItemName")) if isinstance(ref.get("ItemName"), dict) else ref.get("ItemName")
                break
            vfilters = (v.get("filterConfig") or {}).get("filters", []) or []
            for f in vfilters:
                out["filtros"].append(_filter(f, "Visual", pid, vid))
            out["visuales"].append({
                "page_id": pid, "visual_id": vid, "ruta": vj.relative_to(root).as_posix(), "tipo": vtype,
                "titulo": title, "texto": " / ".join(t for t in texts if t.strip()) or btn_text, "oculto": bool(v.get("isHidden")),
                "x": _r(pos.get("x")), "y": _r(pos.get("y")), "z": _r(pos.get("z")), "ancho": _r(pos.get("width")),
                "alto": _r(pos.get("height")), "tab": _r(pos.get("tabOrder")), "recurso": recurso, "grupo": v.get("parentGroupName") or "—", "bindings": bindings, "otros_campos": otros,
                "acciones": acciones, "filtros_visual": len(vfilters),
                "encabezado": obj_prop(vis.get("objects"), "header", "text"),
                "slicer_modo": obj_prop(vis.get("objects"), "data", "mode"),
                "slicer_unico": obj_prop(vis.get("objects"), "selection", "singleSelect"),
                "sync": ((vis.get("syncGroup") or v.get("syncGroup") or {}) or {}).get("groupName"),
                "bookmarks_navegador": obj_prop(vis.get("objects"), "bookmarks", "bookmarkGroup"),
            })
    all_vids = {vv["visual_id"] for vv in out["visuales"]}
    page_ids = {p["page_id"] for p in out["paginas"]}
    for bj in sorted((d / "bookmarks").glob("*.bookmark.json")) if (d / "bookmarks").is_dir() else []:
        b = load_json(bj)
        st = b.get("explorationState", {}) or {}
        sec = st.get("activeSection")
        opts = b.get("options", {}) or {}
        targets = opts.get("targetVisualNames", []) or []
        estados = defaultdict(list)
        for sname, sdata in (st.get("sections", {}) or {}).items():
            for vid, vc in (sdata.get("visualContainers", {}) or {}).items():
                mode = (((vc or {}).get("singleVisual") or {}).get("display") or {}).get("mode") or "visible"
                estados[(sname, mode, vid in all_vids)].append(vid)
        out["bookmarks"].append({"bookmark_id": b.get("name", bj.name.split(".")[0]), "nombre": b.get("displayName"),
                                 "ruta": bj.relative_to(root).as_posix(), "seccion": sec, "seccion_existe": sec in page_ids,
                                 "opciones": ", ".join(f"{k}={v}" for k, v in opts.items() if k != "targetVisualNames") or "—",
                                 "solo_targets": opts.get("applyOnlyToTargetVisuals"),
                                 "targets": targets, "targets_inexistentes": [t for t in targets if t not in all_vids],
                                 "estados": {k: v for k, v in estados.items()}, "campos": field_refs(st)})
        mark(b, sec, "—", "bookmark")
    static = rep / "StaticResources"
    seen = set()
    for item in registered.values():
        decl = item.get("ruta_declarada") or item.get("resource_id") or ""
        cands = [static / (item.get("paquete") or "RegisteredResources") / decl, static / "RegisteredResources" / decl,
                 static / "SharedResources" / decl, static / "SharedResources" / "BaseThemes" / decl]
        path = next((c for c in cands if c.is_file()), None)
        if path:
            seen.add(path.resolve())
            w, h = image_size(path)
            item.update({"ruta": path.relative_to(root).as_posix(), "peso": path.stat().st_size, "ancho": w, "alto": h, "existe": True})
        else:
            item.update({"ruta": "—", "peso": None, "ancho": None, "alto": None, "existe": False})
        out["recursos"].append(item)
    if static.is_dir():
        for f in sorted(static.rglob("*")):
            if f.is_file() and f.resolve() not in seen:
                w, h = image_size(f)
                out["recursos"].append({"resource_id": f.name, "paquete": f.parent.name, "tipo": f.suffix.lstrip(".") or "—",
                                        "ruta": f.relative_to(root).as_posix(), "peso": f.stat().st_size, "ancho": w, "alto": h,
                                        "existe": True, "usado_por": [], "no_registrado": True})
    out["tema_detalle"] = _theme(static, out["tema"])
    return out


def _r(x):
    try:
        return int(round(float(x)))
    except (TypeError, ValueError):
        return x


def _filter(f, ambito, pid, vid):
    refs = field_refs(f.get("field", {}))
    kind, ent_, prop, agg = refs[0] if refs else ("—", "—", "—", None)
    inv = next(iter(find_all(f, "isInvertedSelectionMode")), None)
    return {"filter_id": f.get("name") or "—", "ambito": ambito, "page_id": pid, "visual_id": vid, "tabla": ent_, "campo": prop,
            "tipo": f.get("type") or "—", "condicion": cond_text(f), "oculto": bool(f.get("isHiddenInViewMode")),
            "bloqueado": bool(f.get("isLockedInViewMode")), "invertido": lit(inv) if inv is not None else False}


def _theme(static: Path, tema: dict) -> dict:
    res = {}
    for kind, name in (("base", tema.get("base")), ("personalizado", tema.get("personalizado"))):
        if not name:
            continue
        cands = list(static.glob(f"**/{name}")) + list(static.glob(f"**/{name}.json")) if static.is_dir() else []
        if not cands:
            res[kind] = {"nombre": name, "archivo": "No encontrado en StaticResources"}
            continue
        t = load_json(cands[0])
        fonts = sorted({str(v.get("fontFace")) for v in (t.get("textClasses") or {}).values() if isinstance(v, dict) and v.get("fontFace")})
        res[kind] = {"nombre": t.get("name", name), "archivo": cands[0].as_posix().split("StaticResources/", 1)[-1],
                     "dataColors": ", ".join((t.get("dataColors") or [])[:12]) or "—", "background": t.get("background", "—"),
                     "foreground": t.get("foreground", "—"), "fuentes": ", ".join(fonts) or "—"}
    return res


# =============================================================================================
# Punto de entrada
# =============================================================================================
def read_pbip(root: Path) -> dict:
    root = root.resolve()
    inv = {"raiz": str(root), "pbip": [p.name for p in root.glob("*.pbip")], "advertencias": []}
    reports, models = sorted(root.glob("*.Report")), sorted(root.glob("*.SemanticModel"))
    if not reports:
        inv["advertencias"].append("No se encontró carpeta *.Report.")
    if not models:
        inv["advertencias"].append("No se encontró carpeta *.SemanticModel.")
    rep = read_report(reports[0], root) if reports else {}
    mod = read_model(models[0] / "definition", root) if models and (models[0] / "definition").is_dir() else \
        {"tablas": [], "relaciones": [], "roles": [], "parametros": [], "propiedades": {}, "advertencias": ["Modelo sin definition/ TMDL."]}
    inv.update(rep)
    inv.update({k: v for k, v in mod.items() if k != "advertencias"})
    inv["advertencias"] += rep.get("advertencias", []) + mod.get("advertencias", [])
    inv["report_dir"] = reports[0].name if reports else "—"
    inv["model_dir"] = models[0].name if models else "—"
    if models and (models[0] / ".platform").exists():
        inv.setdefault("metadatos", {})["model_logicalId"] = load_json(models[0] / ".platform").get("config", {}).get("logicalId")
    return inv
