#!/usr/bin/env python3
"""AI-DLC Diccionario de datos (v2.3): inventario de conexiones, tablas y columnas que usan los tableros,
armado a partir de todos los CENSOS, con la versión de práctica de cada tabla para Creación.

Estructura real: si la tabla figura en el catálogo de Athena (exportado de AWS Glue; vive en otro repositorio y su
ruta se indica en <salida>/config.json, clave «catalogo_athena»), sus columnas y tipos salen de ahí (tal como están en la base, antes de cualquier ajuste de un tablero). Si no figura
(fuente aún no migrada), se usa lo que dice el censo y se marca «no verificado en catálogo».

Uso (A = --censos "MCP_POWERBI/02_censo" --salida "MCP_POWERBI/00_dlc/00_diccionario_datos"):
  python scripts/diccionario.py estado     A                       # ¿al día? (no escribe)
  python scripts/diccionario.py actualizar A --correo-ejecutor x   # regenera solo si algún censo cambió
  python scripts/diccionario.py buscar     A --texto "entregas"
  python scripts/diccionario.py impacto    A --objeto "Entregas Totales" [--columna valor]
  python scripts/diccionario.py simulacion A --objeto "Entregas Totales"

Códigos de salida: 0 ok/al día · 10 desactualizado · 11 sin diccionario · 12 objeto no encontrado o ambiguo.
Disparadores en lenguaje natural: ai-dlc/disparadores.md.

Solo lee los censos; nunca los modifica. No se conecta a ninguna base de datos.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from datetime import datetime, timezone, timedelta
from pathlib import Path

VERSION = "2.3"
TZ = timezone(timedelta(hours=-5))
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

# Conectores de base de datos / archivo reconocidos -> motor
CONECTORES = {
    "AmazonAthena.Databases": "Amazon Athena",
    "Sql.Database": "SQL Server",
    "Sql.Databases": "SQL Server",
    "Odbc.DataSource": "ODBC",
    "Odbc.Query": "ODBC",
    "Snowflake.Databases": "Snowflake",
    "Oracle.Database": "Oracle",
    "PostgreSQL.Database": "PostgreSQL",
    "MySQL.Database": "MySQL",
    "GoogleBigQuery.Database": "Google BigQuery",
    "Databricks.Catalogs": "Databricks",
    "Databricks.Contents": "Databricks",
    "AmazonRedshift.Database": "Amazon Redshift",
    "Teradata.Database": "Teradata",
    "SapHana.Database": "SAP HANA",
    "Excel.Workbook": "Archivo Excel",
    "Csv.Document": "Archivo CSV",
    "SharePoint.Files": "SharePoint",
    "SharePoint.Tables": "SharePoint",
    "SharePoint.Contents": "SharePoint",
    "Web.Contents": "Web",
    "Folder.Files": "Carpeta",
}
ARCHIVO = {"Archivo Excel", "Archivo CSV", "SharePoint", "Web", "Carpeta"}

# Tipo TMDL (dataType) -> tipo M
TIPOS_M = {
    "int64": "Int64.Type",
    "string": "type text",
    "datetime": "type datetime",
    "date": "type date",
    "double": "type number",
    "decimal": "Currency.Type",
    "boolean": "type logical",
    "binary": "type binary",
    "datetimezone": "type datetimezone",
    "time": "type time",
}
# Tipo del catálogo (Athena / Glue) -> tipo M
def tipo_m_catalogo(tipo: str) -> str:
    t = (tipo or "").strip().lower()
    if t.startswith(("varchar", "char", "string")):
        return "type text"
    if t in ("bigint", "integer", "int", "smallint", "tinyint"):
        return "Int64.Type"
    if t in ("double", "real", "float") or t.startswith("decimal"):
        return "type number"
    if t == "boolean":
        return "type logical"
    if t.startswith("timestamp"):
        return "type datetime"
    if t == "date":
        return "type date"
    return "type any"


# Familia de un tipo M, para saber si un tablero cambió el tipo real de una columna
FAMILIA_M = {"type text": "texto", "Int64.Type": "número", "type number": "número", "Currency.Type": "número",
             "type logical": "lógico", "type datetime": "fecha", "type date": "fecha", "type datetimezone": "fecha"}

# Nombres que sugieren dato personal (marca automática por nombre; no se confirma aquí)
PII_RE = re.compile(r"(cedula|c[eé]dula|nit\b|^nit$|documento|correo|e-?mail|telefono|tel[eé]fono|celular|"
                    r"direccion|direcci[oó]n|placa|pasaporte|nombretercero|nombre_cliente|cliente_nombre)", re.I)
SECRETO_RE = re.compile(r"(password|pwd|secret|token|accesskey|secretkey|apikey|api_key)\s*[=:]\s*\S", re.I)


# ----------------------------------------------------------------------------- utilidades
def ahora() -> str:
    return datetime.now(TZ).isoformat(timespec="seconds")


def celdas(linea: str) -> list[str]:
    linea = linea.strip()
    if linea.startswith("|"):
        linea = linea[1:]
    if linea.endswith("|"):
        linea = linea[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", linea)]


def es_separador(linea: str) -> bool:
    return bool(re.match(r"^\s*\|?\s*:?-{3,}", linea))


def tablas_md(texto: str) -> list[tuple[list[str], list[list[str]]]]:
    """Devuelve todas las tablas markdown del texto como (encabezados, filas)."""
    lineas = texto.splitlines()
    res, i = [], 0
    while i < len(lineas) - 1:
        if lineas[i].strip().startswith("|") and es_separador(lineas[i + 1]):
            enc = celdas(lineas[i])
            filas, j = [], i + 2
            while j < len(lineas) and lineas[j].strip().startswith("|"):
                filas.append(celdas(lineas[j]))
                j += 1
            res.append((enc, filas))
            i = j
        else:
            i += 1
    return res


def tabla_con(texto: str, columna: str):
    for enc, filas in tablas_md(texto):
        if any(columna.lower() == e.lower() for e in enc):
            return [dict(zip(enc, f)) for f in filas]
    return []


def secciones(texto: str, nivel: int = 1) -> list[tuple[str, str]]:
    """Divide por encabezados del nivel indicado, ignorando bloques de código."""
    marca = "#" * nivel + " "
    partes, titulo, buf, en_codigo = [], "", [], False
    for linea in texto.splitlines():
        if linea.strip().startswith("```"):
            en_codigo = not en_codigo
        if not en_codigo and linea.startswith(marca) and not linea.startswith(marca + "#"):
            partes.append((titulo, "\n".join(buf)))
            titulo, buf = linea[len(marca):].strip(), []
        else:
            buf.append(linea)
    partes.append((titulo, "\n".join(buf)))
    return partes


def seccion(texto: str, *claves: str, nivel: int = 1) -> str:
    for titulo, cuerpo in secciones(texto, nivel):
        t = titulo.lower()
        if any(c.lower() in t for c in claves):
            return cuerpo
    return ""


def limpiar(valor: str) -> str:
    return valor.strip().strip("`").strip()


def cadenas_m(texto: str) -> list[str]:
    return [s.replace('""', '"') for s in re.findall(r'"((?:[^"]|"")*)"', texto)]


def llamada_balanceada(texto: str, inicio: int) -> str:
    """Desde el índice de '(' devuelve el contenido hasta su paréntesis de cierre."""
    nivel, i, en_cadena = 0, inicio, False
    while i < len(texto):
        ch = texto[i]
        if ch == '"':
            if en_cadena and i + 1 < len(texto) and texto[i + 1] == '"':
                i += 2
                continue
            en_cadena = not en_cadena
        elif not en_cadena:
            if ch == "(":
                nivel += 1
            elif ch == ")":
                nivel -= 1
                if nivel == 0:
                    return texto[inicio + 1:i]
        i += 1
    return texto[inicio + 1:]


def slug(texto: str) -> str:
    s = re.sub(r"[^0-9A-Za-z]+", "_", texto).strip("_")
    return s or "objeto"


def tipo_m(tipo: str | None) -> str:
    return TIPOS_M.get((tipo or "").strip().lower(), "type any")


def nombre_m(col: str) -> str:
    return '#"' + col.replace('"', '""') + '"'


def esc(t) -> str:
    return str(t if t not in (None, "") else "—").replace("|", "\\|").replace("\n", " ")


def norm(t: str) -> str:
    t = unicodedata.normalize("NFKD", str(t or "")).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()


def clave_col(nombre: str) -> str:
    """Clave tolerante: el catálogo trae tildes y eñes dañadas («a�o» por «año»); cualquier carácter
    fuera de a-z, 0-9 y _ cuenta como comodín."""
    return re.sub(r"[^a-z0-9_]", "?", (nombre or "").strip().lower())


# ----------------------------------------------------------------------------- catálogo de Athena
def rutas_catalogo(salida: Path) -> list[Path]:
    """Rutas configuradas en <salida>/config.json («catalogo_athena»: una ruta o una lista). Una ruta relativa se
    resuelve desde la raíz del proyecto (MCP_POWERBI), así funciona igual en cualquier equipo."""
    cfg = salida / "config.json"
    if not cfg.exists():
        return []
    valor = json.loads(cfg.read_text(encoding="utf-8-sig")).get("catalogo_athena") or []
    raiz = salida.resolve().parents[1]
    return [p if p.is_absolute() else raiz / p for p in map(Path, [valor] if isinstance(valor, str) else valor)]


def catalogo_faltante(salida: Path) -> list[Path]:
    return [p for p in rutas_catalogo(salida) if not p.is_file()]


# ----------------------------------------------------------------------------- vigencia de los censos
def _modulo_censo():
    """censo_versiones.py del DLC del censo (mismo control de «tablero final» que usa `censo.py vigencia`)."""
    ruta = Path(__file__).resolve().parents[2] / "01_ai-dlc-censo" / "scripts"
    if not (ruta / "censo_versiones.py").exists():
        return None
    if str(ruta) not in sys.path:
        sys.path.insert(0, str(ruta))
    try:
        import censo_versiones  # noqa: PLC0415
        return censo_versiones
    except Exception:  # noqa: BLE001
        return None


def vigencia_censo(ruta: Path, raiz_censos: Path) -> dict | None:
    """¿El censo describe el tablero final (última versión guardada y misma huella)? None si no se puede saber."""
    cv = _modulo_censo()
    if cv is None:
        return None
    versiones = raiz_censos.resolve().parent / "01_bi" / "01_versiones"
    vt = cv.vigencia_tablero(ruta.read_text(encoding="utf-8-sig"), versiones, ruta.parent.name)
    return {"vigente": vt["vigente"], "motivos": vt["motivos"]}


def archivos_catalogo(salida: Path) -> list[Path]:
    return [p for p in rutas_catalogo(salida) if p.is_file()]


def hash_catalogo(salida: Path) -> str:
    h = hashlib.sha256()
    for p in archivos_catalogo(salida):
        h.update(p.name.encode())
        h.update(p.read_bytes())
    return h.hexdigest()[:16] if archivos_catalogo(salida) else ""


def leer_catalogo(salida: Path) -> dict:
    """Devuelve {«esquema.tabla» en minúsculas: {"archivo", "columnas": [(nombre, tipo), …]}}."""
    cat = {}
    for p in archivos_catalogo(salida):
        for titulo, cuerpo in secciones(p.read_text(encoding="utf-8-sig"), 3):
            m = re.fullmatch(r"([\w\-]+)\.([\w\-]+)", titulo.strip())
            if not m:
                continue
            filas = tabla_con(cuerpo, "Columna")
            cols = [(limpiar(f.get("Columna", "")), limpiar(f.get("Tipo", ""))) for f in filas if f.get("Columna")]
            if cols:
                cat[f"{m.group(1)}.{m.group(2)}".lower()] = {"archivo": p.name, "columnas": cols}
    return cat


def clave_catalogo(ob: dict) -> str | None:
    if ob["motor"] != "Amazon Athena":
        return None
    esquema = next((n["Name"] for n in ob["navegacion"] if n["Kind"] in ("Schema", "Database") and n["Name"] != "AwsDataCatalog"), None)
    tabla = next((n["Name"] for n in reversed(ob["navegacion"]) if n["Kind"] in ("Table", "View")), None)
    return f"{esquema}.{tabla}".lower() if esquema and tabla else None


def aplicar_catalogo(ob: dict, cat: dict, avisos: list[str]) -> None:
    """Reemplaza columnas y tipos por los del catálogo, en su orden, conservando lo que dicen los censos."""
    clave = clave_catalogo(ob)
    entrada = cat.get(clave) if clave else None
    if not entrada:
        ob["estructura"] = "Solo censo (no está en el catálogo)"
        return
    ob["estructura"] = f"Catálogo Athena ({entrada['archivo']})"
    previas = {clave_col(k): v for k, v in ob["columnas"].items()}
    nuevas = {}
    for nombre, tipo in entrada["columnas"]:
        col = previas.pop(clave_col(nombre), None)
        if col is None:
            col = nueva_columna(nombre)
        col["tipo_real"] = tipo
        col["en_catalogo"] = True
        nuevas[col["nombre_origen"]] = col  # el censo conserva la tilde correcta si el catálogo la dañó
    for col in previas.values():  # columnas que los tableros cargan pero el catálogo no tiene
        col["en_catalogo"] = False
        nuevas[col["nombre_origen"]] = col
    ob["columnas"] = nuevas
    faltan = [c["nombre_origen"] for c in nuevas.values() if not c["en_catalogo"]]
    if faltan:
        avisos.append(f"{ob['nombre']}: {len(faltan)} columna(s) que usan los tableros no están en el catálogo "
                      f"({', '.join(faltan)}); el catálogo puede estar desactualizado")


def tablas_sin_uso(data: dict, cat: dict) -> dict:
    """Tablas del catálogo que ningún tablero censado usa todavía."""
    usadas = {clave_catalogo(o) for o in data["objetos"]}
    return {k: v for k, v in cat.items() if k not in usadas}


def coincidencias_catalogo(libres: dict, texto: str, exacta: bool = False) -> list[str]:
    q = norm(texto)
    if not q:
        return []
    exactas = [k for k in libres if norm(k) == q or norm(k.split(".", 1)[1]) == q]
    if exactas or exacta:
        return exactas
    return [k for k in libres if q in norm(k)]


def objeto_desde_catalogo(data: dict, clave: str, entrada: dict) -> dict:
    """Arma la ficha de una tabla que solo está en el catálogo, con el mismo DSN de Athena que usan los tableros."""
    esquema, tabla = clave.split(".", 1)
    athena = next((cx for cx in data["conexiones"] if cx["motor"] == "Amazon Athena"), None)
    args = athena["argumentos"] if athena else ["<DSN por confirmar>"]
    cols = {}
    for nombre, tipo in entrada["columnas"]:
        cols[nombre] = {"nombre_origen": nombre, "tipo_m": tipo_m_catalogo(tipo), "tipo_real": tipo,
                        "pii": bool(PII_RE.search(nombre))}
    ob = {"objeto_id": f"amazon_athena:{args[0]}/AwsDataCatalog/{esquema}/{tabla}", "nombre": tabla,
          "conector": "AmazonAthena.Databases", "argumentos": args, "acceso": "Navegación", "sql": None,
          "pasos_nav": [{"registro": 'Name="AwsDataCatalog",Kind="Database"', "campo": "Data", "nombre": "AwsDataCatalog"},
                        {"registro": f'Name="{esquema}",Kind="Schema"', "campo": "Data", "nombre": esquema},
                        # sin Kind: en Athena la tabla puede ser «Table» o «View»
                        {"registro": f'Name="{tabla}"', "campo": "Data", "nombre": tabla}],
          "columnas": cols, "dsn_conocido": athena is not None}
    ob["consulta_sim"], ob["consulta_real"], ob["consulta_src"] = ("Sim_" + slug(tabla), "Real_" + slug(tabla),
                                                                   "Src_" + slug(tabla))
    ob["m_real"], ob["m_simulacion"] = m_real(ob), m_simulacion(ob)
    return ob


# ----------------------------------------------------------------------------- análisis de M
def analizar_m(codigo: str) -> dict:
    info = {"conector": None, "motor": None, "argumentos": [], "navegacion": [], "pasos_nav": [], "sql": None,
            "columnas_quitadas": [], "filtros": [], "compuesto": False}
    # conector (el primero reconocido)
    mejor = None
    for fn in CONECTORES:
        for m in re.finditer(re.escape(fn) + r"\s*\(", codigo):
            if mejor is None or m.start() < mejor[1]:
                mejor = (fn, m.start(), m.end() - 1)
    if mejor:
        fn, _, par = mejor
        args = llamada_balanceada(codigo, par)
        info["conector"] = fn
        info["motor"] = CONECTORES[fn]
        info["argumentos"] = cadenas_m(args)[:1] if fn == "Odbc.Query" else cadenas_m(args.split("[", 1)[0])
        q = re.search(r'Query\s*=\s*"((?:[^"]|"")*)"', args)
        if q:
            info["sql"] = q.group(1).replace('""', '"')
        if fn == "Odbc.Query":
            cs = cadenas_m(args)
            if len(cs) > 1:
                info["sql"] = cs[1]
    nq = re.search(r"Value\.NativeQuery\s*\(", codigo)
    if nq:
        cs = cadenas_m(llamada_balanceada(codigo, nq.end() - 1))
        if cs:
            info["sql"] = cs[0]
    # navegación (se conserva el registro original para reproducirla exactamente)
    for m in re.finditer(r"\{\s*\[([^\]]*)\]\s*\}\s*\[\s*(Data|Content)\s*\]", codigo):
        campos = dict(re.findall(r'(\w+)\s*=\s*"((?:[^"]|"")*)"', m.group(1)))
        info["pasos_nav"].append({"registro": re.sub(r"\s+", " ", m.group(1)).strip(),
                                  "campo": m.group(2), "nombre": campos.get("Item") or campos.get("Name", "")})
        if "Schema" in campos and "Item" in campos:
            info["navegacion"] += [{"Kind": "Schema", "Name": campos["Schema"]}, {"Kind": "Table", "Name": campos["Item"]}]
        elif "Name" in campos:
            info["navegacion"].append({"Kind": campos.get("Kind", "—"), "Name": campos["Name"]})
        elif "Item" in campos:
            info["navegacion"].append({"Kind": campos.get("Kind", "Item"), "Name": campos["Item"]})
    # columnas quitadas
    for m in re.finditer(r"Table\.RemoveColumns\s*\(", codigo):
        cuerpo = llamada_balanceada(codigo, m.end() - 1)
        lista = re.search(r"\{([^}]*)\}", cuerpo)
        info["columnas_quitadas"] += cadenas_m(lista.group(1) if lista else cuerpo.split(",", 1)[-1])
    # filtros de carga
    for m in re.finditer(r'(#"[^"]+"|\w+)\s*=\s*Table\.SelectRows\s*\(', codigo):
        cuerpo = llamada_balanceada(codigo, m.end() - 1)
        cond = cuerpo.split("each", 1)[-1].strip() if "each" in cuerpo else cuerpo
        info["filtros"].append(re.sub(r"\s+", " ", cond))
    # composición (más de un origen o combinaciones): las columnas no se atribuyen automáticamente
    if len(re.findall("|".join(re.escape(c) + r"\s*\(" for c in CONECTORES), codigo)) > 1 or \
            re.search(r"Table\.(NestedJoin|Join|Combine|FuzzyNestedJoin)\s*\(", codigo):
        info["compuesto"] = True
    return info


# ----------------------------------------------------------------------------- lectura de un censo
def leer_censo(ruta: Path) -> dict:
    texto = ruta.read_text(encoding="utf-8-sig")
    c = {"archivo": str(ruta), "bi": None, "census_id": None, "fecha": None, "estado": None,
         "consumible": True, "motivo": "", "fuentes": [], "m": {}, "matriz_a": {},
         "hash": hashlib.sha256(texto.encode()).hexdigest()[:16]}
    for clave, patron in [("census_id", r"census_id:\s*(\S+)"), ("fecha", r"Fecha y hora de ejecución:\s*(\S+)"),
                          ("estado", r"Estado:\s*(.+)")]:
        m = re.search(r"^>\s*" + patron, texto, re.M)
        if m:
            c[clave] = m.group(1).strip()
    for fila in tabla_con(seccion(texto, "Identificación"), "Campo"):
        if fila.get("Campo", "").lower() == "nombre bi":
            c["bi"] = fila.get("Valor")
    if not c["bi"]:
        m = re.search(r"^#\s*Censo BI\s*[—-]\s*(.+)$", texto, re.M)
        c["bi"] = m.group(1).strip() if m else ruta.parent.name

    c["fuentes"] = tabla_con(seccion(texto, "Fuentes de datos"), "fuente_id")
    if not c["fuentes"]:
        c["consumible"] = False
        c["motivo"] = "Censo en formato anterior (sin tabla «fuente_id»): volver a censar con el ritual vigente."
        return c

    for titulo, cuerpo in secciones(seccion(texto, "Transformaciones"), 2):
        m = re.match(r"[\d.]+\s+(.+?)\s*\(partición\s*`([^`]+)`", titulo)
        bloque = re.search(r"```m\s*\n(.*?)```", cuerpo, re.S)
        if m and bloque:
            c["m"][(m.group(1).strip(), m.group(2).strip())] = bloque.group(1)

    for titulo, cuerpo in secciones(seccion(texto, "Columnas"), 3):
        m = re.match(r"(.+?)\s*\(\d+\s+columnas?\)", titulo)
        if m:
            c["matriz_a"][m.group(1).strip()] = tabla_con(cuerpo, "column_id")
    return c


# ----------------------------------------------------------------------------- consolidación
def nueva_columna(nombre: str) -> dict:
    return {"nombre_origen": nombre, "tipos": {}, "nombres_modelo": {}, "quitada_en": [],
            "pii": bool(PII_RE.search(nombre))}


def consolidar(censos: list[dict], cat: dict) -> dict:
    conexiones, objetos, avisos = {}, {}, []

    for c in censos:
        if not c["consumible"]:
            if "más reciente" not in c["motivo"]:
                avisos.append(f"{c['bi']}: {c['motivo']}")
            continue
        for f in c["fuentes"]:
            tabla, part = limpiar(f.get("Tabla del modelo", "")), limpiar(f.get("Partición", ""))
            codigo = c["m"].get((tabla, part)) or next((v for (t, _), v in c["m"].items() if t == tabla), "")
            if not codigo:
                avisos.append(f"{c['bi']}: la tabla «{tabla}» no tiene código M en el censo")
                continue
            info = analizar_m(codigo)
            if not info["conector"]:
                continue  # tabla sin base de datos (embebida, calculada): no es una conexión
            arg0 = info["argumentos"][0] if info["argumentos"] else "—"
            destino = re.sub(r"(?i)^\s*dsn\s*=\s*", "", arg0).split(";")[0].strip()
            conexion_id = f"{slug(info['motor']).lower()}:{destino}"
            if info["sql"] and not info["navegacion"]:
                ruta_obj, acceso = "consulta:" + hashlib.sha256(info["sql"].encode()).hexdigest()[:10], "Consulta nativa"
            else:
                ruta_obj = "/".join(n["Name"] for n in info["navegacion"]) or "/".join(info["argumentos"][1:]) or "—"
                acceso = "Archivo" if info["motor"] in ARCHIVO else "Navegación"
            objeto_id = f"{conexion_id}/{ruta_obj}"

            cx = conexiones.setdefault(conexion_id, {"conexion_id": conexion_id, "motor": info["motor"],
                                                     "conector": info["conector"], "argumentos": info["argumentos"],
                                                     "destino": destino, "bi": [], "objetos": []})
            if c["bi"] not in cx["bi"]:
                cx["bi"].append(c["bi"])
            ob = objetos.get(objeto_id)
            if ob is None:
                ob = objetos[objeto_id] = {
                    "objeto_id": objeto_id, "conexion_id": conexion_id, "motor": info["motor"],
                    "conector": info["conector"], "argumentos": info["argumentos"], "acceso": acceso,
                    "navegacion": info["navegacion"], "pasos_nav": info["pasos_nav"], "sql": info["sql"],
                    "nombre": info["navegacion"][-1]["Name"] if info["navegacion"] else ruta_obj,
                    "columnas": {}, "usos": []}
                cx["objetos"].append(objeto_id)
            ob["usos"].append({"bi": c["bi"], "census_id": c["census_id"], "tabla_modelo": tabla,
                               "filtros_carga": info["filtros"], "columnas_quitadas": info["columnas_quitadas"]})
            if info["compuesto"]:
                avisos.append(f"{c['bi']}: «{tabla}» combina varios orígenes; sus columnas no se atribuyen a {objeto_id}")
                continue
            for fila in c["matriz_a"].get(tabla, []):
                if limpiar(fila.get("Clase", "")).lower() != "origen":
                    continue
                origen = limpiar(fila.get("Nombre en origen", ""))
                if not origen or origen == "—":
                    continue
                col = ob["columnas"].setdefault(origen, nueva_columna(origen))
                t = limpiar(fila.get("Tipo", "")).lower() or "—"
                if c["bi"] not in col["tipos"].setdefault(t, []):
                    col["tipos"][t].append(c["bi"])
                col["nombres_modelo"][c["bi"]] = limpiar(fila.get("Columna", ""))
            for q in info["columnas_quitadas"]:
                col = ob["columnas"].setdefault(q, nueva_columna(q))
                if c["bi"] not in col["quitada_en"]:
                    col["quitada_en"].append(c["bi"])

    for ob in objetos.values():
        aplicar_catalogo(ob, cat, avisos)
        for col in ob["columnas"].values():
            tipos = [t for t in col["tipos"] if t != "—"]
            col["tipo"] = tipos[0] if len(tipos) == 1 else None  # tipo en los tableros; None = desconocido o distinto
            col.setdefault("tipo_real", None)
            col.setdefault("en_catalogo", None)
            col["tipo_m"] = tipo_m_catalogo(col["tipo_real"]) if col["tipo_real"] else tipo_m(col["tipo"])
            # tableros que cambian el tipo real (ej.: texto -> número)
            col["cambiado_en"] = []
            if col["tipo_real"]:
                real = FAMILIA_M.get(col["tipo_m"])
                for t, bis in col["tipos"].items():
                    fam = FAMILIA_M.get(tipo_m(t))
                    if real and fam and fam != real:
                        col["cambiado_en"] += [(b, t) for b in bis]
        if not ob["columnas"]:
            avisos.append(f"{ob['objeto_id']}: sin columnas atribuidas; no se puede simular")
        ob["consulta_sim"] = "Sim_" + slug(ob["nombre"])
        ob["consulta_real"] = "Real_" + slug(ob["nombre"])
        ob["consulta_src"] = "Src_" + slug(ob["nombre"])
        ob["m_real"] = m_real(ob)
        ob["m_simulacion"] = m_simulacion(ob)
    return {"conexiones": conexiones, "objetos": objetos, "avisos": avisos}


def m_real(ob: dict) -> str:
    args = ", ".join('"' + a.replace('"', '""') + '"' for a in ob["argumentos"])
    if ob["acceso"] == "Consulta nativa":
        sql = (ob["sql"] or "").replace('"', '""')
        if ob["conector"] == "Odbc.Query":
            return f'let\n    Origen = Odbc.Query({args}, "{sql}")\nin\n    Origen'
        return (f'let\n    Servidor = {ob["conector"]}({args}),\n'
                f'    Origen = Value.NativeQuery(Servidor, "{sql}", null, [EnableFolding = true])\nin\n    Origen')
    extra = ", null, []" if ob["conector"] == "AmazonAthena.Databases" else ""
    lineas, anterior = [f'    Origen = {ob["conector"]}({args}{extra})'], "Origen"
    for i, n in enumerate(ob["pasos_nav"], 1):
        paso = f'Nav{i}_{slug(n["nombre"])}'
        lineas.append(f'    {paso} = {anterior}{{[{n["registro"]}]}}[{n["campo"]}]')
        anterior = paso
    return "let\n" + ",\n".join(lineas) + f"\nin\n    {anterior}"


def m_simulacion(ob: dict) -> str:
    cols = list(ob["columnas"].values())
    if not cols:
        return "// Sin columnas atribuidas: no se puede simular esta tabla."
    filas = ",\n".join(f"            {nombre_m(c['nombre_origen'])} = {c['tipo_m']}" for c in cols)
    return ("// Versión de práctica: estructura real del origen (catálogo de Athena o, si no está, censos); 0 filas. "
            "No contiene datos.\n"
            "let\n    Fuente = #table(\n        type table [\n" + filas + "\n        ],\n        {}\n    )\nin\n    Fuente")


# ----------------------------------------------------------------------------- salida
def tipo_texto(col: dict) -> str:
    if col["tipo_real"]:
        return col["tipo_real"]
    if col["en_catalogo"] is False:
        base = "⚠ No está en el catálogo"
    else:
        base = "No verificado en catálogo"
    if col["tipo"]:
        return f"{base} (en el tablero: {col['tipo']})"
    if len(col["tipos"]) > 1:
        return f"{base} (distinto entre tableros: " + "; ".join(f"{t} en {', '.join(b)}" for t, b in col["tipos"].items()) + ")"
    return f"{base} (desconocido)"


def generar_md(d: dict, censos: list[dict], ejecutor: str) -> str:
    o = []
    w = o.append
    usados = [c for c in censos if c["consumible"]]
    w("# Diccionario de datos — Fuentes de los tableros\n")
    w(f"> diccionario_id: {d['diccionario_id']} · generado {d['generado']} por {ejecutor} · versión {VERSION}\n>\n"
      f"> Censos usados: " + ", ".join(f"{c['bi']} ({c['census_id']}"
                                       + ("; ⚠ NO describe el tablero final" if c.get("vigente") is False else "") + ")"
                                       for c in usados) + "\n")
    w("La estructura es la **real de la base**, antes de cualquier ajuste de un tablero: si la tabla está en el "
      "catálogo de Athena, columnas y tipos salen de ahí; si no (fuente aún no migrada), salen del censo y se marcan "
      "«no verificado en catálogo». No se registran datos ni contraseñas. Aquí aparecen las tablas que algún "
      "tablero censado usa.\n")
    if d.get("libres"):
        w(f"**Para tableros nuevos:** el catálogo de Athena tiene además **{d['libres']} tablas que ningún tablero usa "
          "todavía**. No se listan aquí, pero se encuentran con «busca fuente …» y se puede preparar su versión de "
          "práctica igual que las demás.\n")

    w("## 1. Conexiones\n")
    w("| Conexión | Tipo de conexión | Servidor / DSN | Tablas | Tableros que la usan |\n|---|---|---|---:|---|")
    for cx in sorted(d["conexiones"].values(), key=lambda x: x["conexion_id"]):
        w(f"| `{cx['conexion_id']}` | {cx['motor']} (`{cx['conector']}`) | {esc(cx['destino'])} | "
          f"{len(cx['objetos'])} | {esc(', '.join(cx['bi']))} |")
    w("")

    w("## 2. Tablas\n")
    w("| Tabla | Conexión | Ruta | Columnas | Estructura tomada de | Tableros que la usan |\n|---|---|---|---:|---|---|")
    obs = sorted(d["objetos"].values(), key=lambda x: x["objeto_id"])
    for ob in obs:
        ruta = " / ".join(x["Name"] for x in ob["navegacion"]) or ob["acceso"]
        w(f"| **{ob['nombre']}** | `{ob['conexion_id']}` | {esc(ruta)} | {len(ob['columnas'])} | {esc(ob['estructura'])} | "
          f"{esc(', '.join(sorted({u['bi'] for u in ob['usos']})))} |")
    w("")

    w("## 3. Columnas por tabla\n")
    for n, ob in enumerate(obs, 1):
        w(f"### 3.{n} {ob['nombre']}\n")
        w(f"Referencia: `{ob['objeto_id']}` · versión de práctica `simulacion/{ob['consulta_sim']}.m` · "
          f"conexión real `simulacion/{ob['consulta_real']}.m`\n")
        if ob["sql"]:
            w(f"Consulta nativa:\n\n```sql\n{ob['sql']}\n```\n")
        w("| Columna | Tipo real | Nombre en los tableros | Posible dato personal |\n|---|---|---|---|")
        for col in ob["columnas"].values():
            cambios = dict(col["cambiado_en"])
            nombres = [f"{v} ({k}" + (f", lo cambia a {cambios[k]})" if k in cambios else ")")
                       for k, v in col["nombres_modelo"].items()]
            nombres += [f"quitada en {b}" for b in col["quitada_en"]]
            if not nombres:
                nombres = ["ningún tablero la usa"]
            w(f"| `{col['nombre_origen']}` | {esc(tipo_texto(col))} | {esc('; '.join(nombres))} | "
              f"{'Sí (por el nombre)' if col['pii'] else '—'} |")
        w("")
        w("Tableros que la usan (sus filtros son reglas de ese tablero; no se heredan sin aprobación):\n")
        for u in ob["usos"]:
            filtros = "; ".join(u["filtros_carga"]) or "sin filtros"
            w(f"- **{u['bi']}** (tabla «{u['tabla_modelo']}»): filtros de carga: {filtros}")
        w("")

    if d["avisos"]:
        w("## Avisos\n")
        for a in d["avisos"]:
            w(f"- {a}")
        w("")
    return "\n".join(o) + "\n"


# ----------------------------------------------------------------------------- vigencia
def buscar_censos(raiz: Path) -> list[Path]:
    """Solo el censo vigente de cada tablero: <raiz>/<BI>/<BI> - censo.md. Quedan fuera los borradores abiertos,
    los censos archivados en versiones/, el historial y el registro de revisiones."""
    return sorted(p for p in raiz.glob("*/* - censo.md") if p.name == f"{p.parent.name} - censo.md")


def clave_censo(p: Path, raiz: Path) -> str:
    try:
        return p.resolve().relative_to(raiz.resolve()).as_posix()
    except ValueError:
        return p.as_posix()


def hash_censo(p: Path) -> str:
    return hashlib.sha256(p.read_text(encoding="utf-8-sig").encode()).hexdigest()[:16]


def cargar(salida: Path) -> dict | None:
    js = salida / "diccionario-datos.json"
    return json.loads(js.read_text(encoding="utf-8")) if js.exists() else None


def diagnostico(raiz: Path, salida: Path) -> dict:
    """Compara los censos actuales con los que usó el diccionario. No escribe nada."""
    dg = {"existe": False, "nuevos": [], "modificados": [], "eliminados": [], "sin_cambios": [],
          "estado": "SIN_DICCIONARIO", "diccionario_id": None, "generado": None}
    actuales = {clave_censo(p, raiz): hash_censo(p) for p in buscar_censos(raiz)}
    data = cargar(salida)
    if data is None:
        dg["nuevos"] = sorted(actuales)
        return dg
    dg.update(existe=True, diccionario_id=data["diccionario_id"], generado=data["generado"])
    usados = {c["archivo"]: c["hash"] for c in data["censos"]}
    for ruta, h in sorted(actuales.items()):
        if ruta not in usados:
            dg["nuevos"].append(ruta)
        elif usados[ruta] != h:
            dg["modificados"].append(ruta)
        else:
            dg["sin_cambios"].append(ruta)
    dg["eliminados"] = sorted(set(usados) - set(actuales))
    dg["catalogo_falta"] = [str(p) for p in catalogo_faltante(salida)]
    # si el catálogo no se encuentra en este equipo no se toma como «cambio»: regenerar lo degradaría
    dg["catalogo_cambio"] = not dg["catalogo_falta"] and data.get("hash_catalogo", "") != hash_catalogo(salida)
    # un censo que deja (o vuelve a) describir el tablero final también cambia el diccionario
    previa = {c["archivo"]: c.get("vigente") for c in data["censos"]}
    dg["vigencia_cambio"] = []
    for p in buscar_censos(raiz):
        clave = clave_censo(p, raiz)
        v = vigencia_censo(p, raiz)
        if v is not None and clave in previa and previa[clave] is not None and previa[clave] != v["vigente"]:
            dg["vigencia_cambio"].append(clave)
    cambio = (dg["nuevos"] or dg["modificados"] or dg["eliminados"] or dg["catalogo_cambio"]
              or dg["vigencia_cambio"] or data.get("version") != VERSION)
    dg["estado"] = "DESACTUALIZADO" if cambio else "AL_DIA"
    return dg


def imprimir_diagnostico(dg: dict) -> None:
    print(f"ESTADO: {dg['estado']}")
    if dg["existe"]:
        print(f"Diccionario: {dg['diccionario_id']} (generado {dg['generado']})")
    for titulo, clave in (("Censos nuevos", "nuevos"), ("Censos modificados", "modificados"),
                          ("Censos eliminados", "eliminados")):
        if dg[clave]:
            print(f"{titulo} ({len(dg[clave])}):")
            for r in dg[clave]:
                print(f"  - {r}")
    print(f"Censos sin cambios: {len(dg['sin_cambios'])}")
    if dg.get("catalogo_cambio"):
        print("El catálogo de Athena cambió y aún no está incorporado.")
    for p in dg.get("catalogo_falta", []):
        print(f"AVISO: no se encuentra el catálogo de Athena en {p} (revisar config.json).")
    for r in dg.get("vigencia_cambio", []):
        print(f"Cambió la vigencia del censo {r} (se guardó una versión nueva del tablero o se volvió a censar).")


CODIGO_ESTADO = {"AL_DIA": 0, "DESACTUALIZADO": 10, "SIN_DICCIONARIO": 11}


def exigir_vigente(a) -> tuple[dict | None, int]:
    """Las consultas solo responden con un diccionario al día (o si se permite explícitamente)."""
    dg = diagnostico(Path(a.censos), Path(a.salida))
    if dg["estado"] != "AL_DIA" and not a.permitir_desactualizado:
        imprimir_diagnostico(dg)
        print("DETENIDO: el diccionario no está al día. Ejecutar «actualizar» antes de consultar.")
        return None, CODIGO_ESTADO[dg["estado"]]
    if dg["estado"] != "AL_DIA":
        print(f"AVISO: respuesta sobre un diccionario {dg['estado']}.")
    return cargar(Path(a.salida)), 0


def resolver_objeto(data: dict, texto: str) -> list[dict]:
    objs = [o for o in data["objetos"] if o["objeto_id"] == texto]
    if not objs:
        q = norm(texto)
        objs = [o for o in data["objetos"]
                if any(q and q in norm(c) for c in [o["objeto_id"], o["nombre"]] + [u["tabla_modelo"] for u in o["usos"]])]
    return objs


def elegir_objeto(data: dict, texto: str):
    objs = resolver_objeto(data, texto)
    if not objs:
        print(f"NO ENCONTRADO: «{texto}» no está en el diccionario ni en el catálogo de Athena. "
              f"Aplicar el disparador «fuente nueva».")
        return None
    if len(objs) > 1:
        print(f"AMBIGUO: «{texto}» coincide con {len(objs)} tablas; pedir al usuario que elija:")
        for o in objs:
            print(f"  - {o['objeto_id']} (tableros: {', '.join(sorted({u['bi'] for u in o['usos']}))})")
        return None
    return objs[0]


# ----------------------------------------------------------------------------- comandos
def cmd_estado(a) -> int:
    dg = diagnostico(Path(a.censos), Path(a.salida))
    imprimir_diagnostico(dg)
    return CODIGO_ESTADO[dg["estado"]]


def cmd_actualizar(a) -> int:
    if not EMAIL_RE.match(a.correo_ejecutor or ""):
        print("ERROR: falta un correo válido de quien actualiza (--correo-ejecutor). No se inicia.")
        return 2
    raiz, salida = Path(a.censos), Path(a.salida)
    dg = diagnostico(raiz, salida)
    imprimir_diagnostico(dg)
    if dg.get("catalogo_falta") and not a.sin_catalogo:
        print("DETENIDO: no se encuentra el catálogo de Athena configurado; regenerar sin él perdería los tipos reales. "
              "Corregir la ruta en config.json (o usar --sin-catalogo si es intencional).")
        return 4
    if dg["estado"] == "AL_DIA" and not a.forzar:
        print("SIN CAMBIOS: no se regenera el diccionario.")
        return 0
    archivos = buscar_censos(raiz)
    if not archivos:
        print(f"ERROR: no se encontraron censos en {raiz}")
        return 2
    censos = [leer_censo(p) for p in archivos]
    for c, p in zip(censos, archivos):
        c["archivo"] = clave_censo(p, raiz)
        v = vigencia_censo(p, raiz)
        c["vigente"] = v["vigente"] if v else None
        c["motivos_vigencia"] = v["motivos"] if v else []
    # solo el censo más reciente de cada tablero
    ultimo = {}
    for c in censos:
        if c["bi"] not in ultimo or (c["fecha"] or "") > (ultimo[c["bi"]]["fecha"] or ""):
            ultimo[c["bi"]] = c
    for c in censos:
        if ultimo[c["bi"]] is not c:
            c["consumible"], c["motivo"] = False, "Existe un censo más reciente del mismo tablero."

    for p in rutas_catalogo(salida):
        if not p.is_file():
            print(f"AVISO: no se encontró el catálogo de Athena en {p} (revisar config.json).")
    cat = leer_catalogo(salida)
    if not cat:
        print("AVISO: sin catálogo de Athena; columnas y tipos salen solo de los censos.")
    d = consolidar(censos, cat)
    for c in censos:
        if c["consumible"] and c["vigente"] is False:
            d["avisos"].insert(0, f"{c['bi']}: el censo NO describe el tablero final ({' '.join(c['motivos_vigencia'])}) "
                                  "Sus fuentes pueden estar desactualizadas: volver a censar el tablero.")
    d["generado"] = ahora()
    d["diccionario_id"] = datetime.now(TZ).strftime("%Y%m%dT%H%M%S") + "-diccionario"
    d["libres"] = len(set(cat) - {clave_catalogo(o) for o in d["objetos"].values()})
    md = generar_md(d, censos, a.correo_ejecutor)
    if SECRETO_RE.search(md):
        print("ERROR: el resultado contiene un patrón de credencial. Revisar los censos; no se escribe nada.")
        return 3
    salida.mkdir(parents=True, exist_ok=True)
    (salida / "diccionario-datos.md").write_text(md, encoding="utf-8")
    data = {"diccionario_id": d["diccionario_id"], "generado": d["generado"], "version": VERSION,
            "ejecutor": a.correo_ejecutor,
            "censos": [{k: c[k] for k in ("bi", "census_id", "fecha", "estado", "consumible", "motivo", "archivo", "hash",
                                          "vigente", "motivos_vigencia")}
                       for c in censos],
            "conexiones": list(d["conexiones"].values()), "objetos": list(d["objetos"].values()), "avisos": d["avisos"],
            "hash_catalogo": hash_catalogo(salida), "tablas_en_catalogo": len(cat)}
    (salida / "diccionario-datos.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    sim = salida / "simulacion"
    sim.mkdir(exist_ok=True)
    vigentes = set()
    for ob in d["objetos"].values():
        for nombre, m in ((ob["consulta_sim"], ob["m_simulacion"]), (ob["consulta_real"], ob["m_real"])):
            (sim / f"{nombre}.m").write_text(m + "\n", encoding="utf-8")
            vigentes.add(f"{nombre}.m")
    # versiones de práctica de tablas que ya ningún tablero usa: se retiran para que Creación no tome obsoletas
    obsoletos = [p for p in list(sim.glob("Sim_*.m")) + list(sim.glob("Real_*.m")) if p.name not in vigentes]
    for p in obsoletos:
        p.unlink()
    if obsoletos:
        print(f"Retiradas {len(obsoletos)} consulta(s) de práctica obsoletas: {', '.join(p.name for p in obsoletos)}")
    print(f"ACTUALIZADO: {d['diccionario_id']}")
    print(f"Censos usados: {sum(c['consumible'] for c in censos)} · conexiones: {len(d['conexiones'])} · "
          f"tablas: {len(d['objetos'])} · columnas: {sum(len(o['columnas']) for o in d['objetos'].values())}")
    en_cat = sum(1 for o in d["objetos"].values() if o["estructura"].startswith("Catálogo"))
    print(f"Estructura real desde el catálogo: {en_cat} de {len(d['objetos'])} tabla(s) "
          f"(catálogo con {len(cat)} tablas)")
    for av in d["avisos"]:
        print(f"AVISO: {av}")
    return 0


def cmd_buscar(a) -> int:
    data, rc = exigir_vigente(a)
    if data is None:
        return rc
    q = norm(a.texto)
    hallados = 0
    for o in data["objetos"]:
        motivos = []
        if q in norm(o["objeto_id"]) or q in norm(o["nombre"]):
            motivos.append("nombre de la tabla")
        for u in o["usos"]:
            if q in norm(u["tabla_modelo"]):
                motivos.append(f"tabla «{u['tabla_modelo']}» en {u['bi']}")
        cols = [c for c in o["columnas"].values()
                if q in norm(c["nombre_origen"]) or any(q in norm(v) for v in c["nombres_modelo"].values())]
        if cols:
            motivos.append("columnas: " + ", ".join(c["nombre_origen"] for c in cols[:20]) + (" …" if len(cols) > 20 else ""))
        if motivos:
            hallados += 1
            bis = ", ".join(sorted({u["bi"] for u in o["usos"]}))
            print(f"\nTABLA {o['nombre']} ({o['objeto_id']})\n  Tableros: {bis}\n  Coincide en: " + "; ".join(motivos))
    print(f"\nRESULTADO: {hallados} tabla(s) usadas por tableros para «{a.texto}».")

    # tablas del catálogo de Athena que ningún tablero usa todavía
    libres = tablas_sin_uso(data, leer_catalogo(Path(a.salida)))
    en_cat = []
    for k, v in sorted(libres.items()):
        motivos = ["nombre de la tabla"] if q in norm(k) else []
        cols = [n for n, _ in v["columnas"] if q in norm(n)]
        if cols:
            motivos.append("columnas: " + ", ".join(cols[:10]) + (" …" if len(cols) > 10 else ""))
        if motivos:
            en_cat.append((k, len(v["columnas"]), motivos))
    if en_cat:
        print(f"\nEN EL CATÁLOGO DE ATHENA, SIN USO EN TABLEROS ({len(en_cat)}):")
        for k, n, motivos in en_cat[:a.limite]:
            print(f"  - {k} ({n} columnas) · coincide en: " + "; ".join(motivos))
        if len(en_cat) > a.limite:
            print(f"  … y {len(en_cat) - a.limite} más (afinar la búsqueda o usar --limite).")
    if not hallados and not en_cat:
        print("No está en el diccionario ni en el catálogo: aplicar el disparador «fuente nueva» (no inventar la conexión).")
    return 0


def cmd_impacto(a) -> int:
    data, rc = exigir_vigente(a)
    if data is None:
        return rc
    if not resolver_objeto(data, a.objeto):
        libres = tablas_sin_uso(data, leer_catalogo(Path(a.salida)))
        cands = coincidencias_catalogo(libres, a.objeto)
        if cands:
            print(f"SIN USO: ningún tablero censado usa {', '.join(cands[:10])}; un cambio ahí no afecta tableros conocidos.")
            return 0
    o = elegir_objeto(data, a.objeto)
    if o is None:
        return 12
    print(f"TABLA {o['nombre']} ({o['objeto_id']})")
    if a.columna:
        q = norm(a.columna)
        col = next((c for c in o["columnas"].values() if norm(c["nombre_origen"]) == q
                    or any(norm(v) == q for v in c["nombres_modelo"].values())), None)
        if col is None:
            print(f"NO ENCONTRADA: la columna «{a.columna}» no figura en la tabla.")
            return 12
        print(f"COLUMNA {col['nombre_origen']} · tipo real {tipo_texto(col)}")
        cambios = dict(col["cambiado_en"])
        for bi, nombre in col["nombres_modelo"].items():
            print(f"  - {bi}: la carga como «{nombre}»" + (f" y la cambia a {cambios[bi]}" if bi in cambios else ""))
        for bi in col["quitada_en"]:
            print(f"  - {bi}: la quita al cargar")
        nombres = {norm(col["nombre_origen"])} | {norm(v) for v in col["nombres_modelo"].values()}
        for u in o["usos"]:
            for f in u["filtros_carga"]:
                if any(n and n in norm(f) for n in nombres):
                    print(f"  - {u['bi']}: filtro de carga: {f}")
    else:
        for u in o["usos"]:
            filtros = "; ".join(u["filtros_carga"]) or "sin filtros"
            print(f"  - {u['bi']} ({u['census_id']}): tabla «{u['tabla_modelo']}», filtros de carga: {filtros}")
    print("ALCANCE: el diccionario dice qué tableros traen la tabla o columna. En qué gráfica exacta se usa está "
          "en el censo de cada tablero listado.")
    return 0


def cmd_simulacion(a) -> int:
    data, rc = exigir_vigente(a)
    if data is None:
        return rc
    solo_catalogo = False
    if resolver_objeto(data, a.objeto):
        o = elegir_objeto(data, a.objeto)
    else:
        cat = leer_catalogo(Path(a.salida))
        libres = tablas_sin_uso(data, cat)
        cands = coincidencias_catalogo(libres, a.objeto)
        if len(cands) > 1:
            print(f"AMBIGUO: «{a.objeto}» coincide con {len(cands)} tablas del catálogo; pedir al usuario que elija:")
            for k in cands[:30]:
                print(f"  - {k}")
            return 12
        o = objeto_desde_catalogo(data, cands[0], libres[cands[0]]) if cands else elegir_objeto(data, a.objeto)
        solo_catalogo = bool(cands)
    if o is None:
        return 12
    print(f"// Tabla: {o['objeto_id']}\n// Diccionario: {data['diccionario_id']}\n")
    if solo_catalogo:
        print("// ATENCIÓN: ningún tablero usa esta tabla todavía. Estructura tomada solo del catálogo de Athena.")
        print("// La conexión real usa el mismo DSN de Athena que los tableros: verificarla en el paso 5 de Creación."
              if o["dsn_conocido"] else "// No hay un DSN de Athena conocido: pedir el DSN (sin contraseñas) antes de liberar.")
        print()
    print('// Parámetro (una vez por BI)\nModoSimulacion = true meta [IsParameterQuery = true, Type = "Logical", IsParameterQueryRequired = true]\n')
    print(f"// {o['consulta_sim']}\n{o['m_simulacion']}\n")
    print(f"// {o['consulta_real']}\n{o['m_real']}\n")
    print(f"// {o['consulta_src']}\nlet\n    Fuente = if ModoSimulacion then {o['consulta_sim']} else {o['consulta_real']}\nin\n    Fuente")
    pii = [c["nombre_origen"] for c in o["columnas"].values() if c["pii"]]
    if pii:
        print("\n// ATENCIÓN: posibles datos personales (decidir con el dueño antes de incluirlos): " + ", ".join(pii))
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    comandos = {
        "estado": "Dice si el diccionario está al día con los censos (no escribe).",
        "actualizar": "Regenera el diccionario solo si algún censo es nuevo, cambió o se eliminó.",
        "buscar": "Busca una tabla o columna (en los tableros y en el catálogo de Athena).",
        "impacto": "Qué tableros traen una tabla o columna.",
        "simulacion": "Consultas Sim_/Real_/Src_ de una tabla para Creación (también tablas solo del catálogo).",
    }
    for nombre, ayuda in comandos.items():
        s = sub.add_parser(nombre, help=ayuda)
        s.add_argument("--censos", required=True, help="Carpeta raíz de los censos (MCP_POWERBI/02_censo)")
        s.add_argument("--salida", required=True, help="Carpeta del diccionario (MCP_POWERBI/00_dlc/00_diccionario_datos)")
        if nombre == "actualizar":
            s.add_argument("--correo-ejecutor", required=True)
            s.add_argument("--forzar", action="store_true", help="Regenerar aunque no haya cambios")
            s.add_argument("--sin-catalogo", action="store_true",
                           help="Regenerar aunque el catálogo configurado no se encuentre (pierde los tipos reales)")
        if nombre == "buscar":
            s.add_argument("--texto", required=True)
            s.add_argument("--limite", type=int, default=25, help="Máximo de tablas del catálogo a listar")
        if nombre in ("impacto", "simulacion"):
            s.add_argument("--objeto", required=True, help="Nombre de la tabla en origen, en un tablero, o su referencia")
        if nombre == "impacto":
            s.add_argument("--columna")
        if nombre in ("buscar", "impacto", "simulacion"):
            s.add_argument("--permitir-desactualizado", action="store_true",
                           help="Responder aunque el diccionario no esté al día (se avisa)")
    a = p.parse_args()
    return {"estado": cmd_estado, "actualizar": cmd_actualizar, "buscar": cmd_buscar,
            "impacto": cmd_impacto, "simulacion": cmd_simulacion}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
