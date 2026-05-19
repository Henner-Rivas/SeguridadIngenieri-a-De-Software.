"""Punto 3: Validar entradas para prevenir inyecciones SQL (simulado)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List

SAFE_QUERY_PATTERN = re.compile(
    r"^\s*(SELECT|UPDATE|DELETE|INSERT)\b(.+)$",
    re.IGNORECASE,
)
SELECT_PATTERN = re.compile(
    r"^SELECT\s+.+?\s+FROM\s+usuarios\s+WHERE\s+nombre\s*=\s*'([A-Za-z0-9_]+)'\s*$",
    re.IGNORECASE,
)
DELETE_PATTERN = re.compile(
    r"^DELETE\s+FROM\s+usuarios\s+WHERE\s+nombre\s*=\s*'([A-Za-z0-9_]+)'\s*$",
    re.IGNORECASE,
)
UPDATE_PATTERN = re.compile(
    r"^UPDATE\s+usuarios\s+SET\s+rol\s*=\s*'([A-Za-z0-9_]+)'\s+WHERE\s+nombre\s*=\s*'([A-Za-z0-9_]+)'\s*$",
    re.IGNORECASE,
)
INSERT_PATTERN = re.compile(
    r"^INSERT\s+INTO\s+usuarios\s*\(\s*nombre\s*,\s*rol\s*\)\s*VALUES\s*\(\s*'([A-Za-z0-9_]+)'\s*,\s*'([A-Za-z0-9_]+)'\s*\)\s*$",
    re.IGNORECASE,
)
FORBIDDEN_PATTERN = re.compile(
    r"('|\")\s*OR\s*('|\")?1('|\")?=\s*('|\")?1|--|;|/\*|\*/",
    re.IGNORECASE,
)


@dataclass
class QueryResult:
    ok: bool
    message: str
    results: List[Dict[str, str]]


def _fake_db() -> List[Dict[str, str]]:
    return [
        {"nombre": "admin", "rol": "Admin"},
        {"nombre": "maria", "rol": "Usuario"},
        {"nombre": "juan", "rol": "Usuario"},
    ]


def validate_query(query: str) -> tuple[bool, str, Dict[str, str] | None]:
    if FORBIDDEN_PATTERN.search(query):
        return False, "Consulta rechazada: patron inseguro detectado", None

    if not SAFE_QUERY_PATTERN.match(query):
        return False, "Consulta rechazada: formato no permitido", None

    select_match = SELECT_PATTERN.match(query)
    if select_match:
        return True, "Consulta valida", {"action": "select", "nombre": select_match.group(1)}

    delete_match = DELETE_PATTERN.match(query)
    if delete_match:
        return True, "Consulta valida", {"action": "delete", "nombre": delete_match.group(1)}

    update_match = UPDATE_PATTERN.match(query)
    if update_match:
        return True, "Consulta valida", {
            "action": "update",
            "rol": update_match.group(1),
            "nombre": update_match.group(2),
        }

    insert_match = INSERT_PATTERN.match(query)
    if insert_match:
        return True, "Consulta valida", {
            "action": "insert",
            "nombre": insert_match.group(1),
            "rol": insert_match.group(2),
        }

    return False, "Consulta rechazada: formato no permitido", None


def run_query(query: str, database: List[Dict[str, str]]) -> QueryResult:
    ok, message, payload = validate_query(query)
    if not ok:
        return QueryResult(False, message, [])

    if payload is None:
        return QueryResult(False, "Consulta rechazada", [])

    action = payload["action"]
    if action == "select":
        username = payload["nombre"]
        results = [row for row in database if row["nombre"] == username]
        if not results:
            return QueryResult(True, "Sin resultados", [])
        return QueryResult(True, "Resultados encontrados", results)

    if action == "delete":
        username = payload["nombre"]
        before = len(database)
        database[:] = [row for row in database if row["nombre"] != username]
        deleted = before - len(database)
        return QueryResult(True, f"Registros eliminados: {deleted}", [])

    if action == "update":
        username = payload["nombre"]
        new_role = payload["rol"]
        updated = 0
        for row in database:
            if row["nombre"] == username:
                row["rol"] = new_role
                updated += 1
        return QueryResult(True, f"Registros actualizados: {updated}", [])

    if action == "insert":
        username = payload["nombre"]
        role = payload["rol"]
        exists = any(row["nombre"] == username for row in database)
        if exists:
            return QueryResult(True, "Usuario ya existe", [])
        database.append({"nombre": username, "rol": role})
        return QueryResult(True, "Usuario insertado", [])

    return QueryResult(True, "Consulta ejecutada", [])


def _demo() -> None:
    database = _fake_db()
    print("Base simulada: usuarios = admin, maria, juan")
    print("Ejemplos validos:")
    print("SELECT * FROM usuarios WHERE nombre = 'admin'")
    print("select nombre, rol from usuarios where nombre='admin'")
    print("UPDATE usuarios SET rol='Admin' WHERE nombre='maria'")
    print("DELETE FROM usuarios WHERE nombre='juan'")
    print("INSERT INTO usuarios (nombre, rol) VALUES ('luis', 'Usuario')")

    query = input("\nConsulta: ").strip()
    result = run_query(query, database)

    print(result.message)
    if result.results:
        for row in result.results:
            print(f"- nombre: {row['nombre']}, rol: {row['rol']}")


if __name__ == "__main__":
    _demo()
