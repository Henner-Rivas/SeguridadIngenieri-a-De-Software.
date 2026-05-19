"""Punto 5: Sistema de roles y permisos (Admin/Usuario)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

try:
    import bcrypt
except ImportError as exc:  # pragma: no cover - runtime guard
    raise SystemExit(
        "Falta instalar dependencia: python3 -m pip install -r requirements.txt"
    ) from exc


@dataclass
class AccessResult:
    ok: bool
    message: str


class RoleAccessControl:
    def __init__(self) -> None:
        self._role_permissions: Dict[str, List[str]] = {
            "Admin": ["Crear datos", "Leer datos", "Editar datos", "Eliminar datos"],
            "Editor": ["Leer datos", "Editar datos"],
            "Usuario": ["Leer datos"],
        }

    def can_access(self, role: str, resource: str) -> AccessResult:
        permissions = self._role_permissions.get(role)
        if permissions is None:
            return AccessResult(False, "Rol no reconocido")
        if resource in permissions:
            return AccessResult(True, "Acceso permitido")
        return AccessResult(False, "Acceso denegado")


class InMemoryDataStore:
    def __init__(self) -> None:
        self._records: List[Dict[str, str]] = [
            {"id": "1", "contenido": "Registro inicial"},
            {"id": "2", "contenido": "Dato de prueba"},
        ]

    def list_records(self) -> List[Dict[str, str]]:
        return list(self._records)

    def create_record(self, content: str) -> Dict[str, str]:
        new_id = str(len(self._records) + 1)
        record = {"id": new_id, "contenido": content}
        self._records.append(record)
        return record

    def update_record(self, record_id: str, content: str) -> bool:
        for record in self._records:
            if record["id"] == record_id:
                record["contenido"] = content
                return True
        return False

    def delete_record(self, record_id: str) -> bool:
        before = len(self._records)
        self._records = [r for r in self._records if r["id"] != record_id]
        return len(self._records) < before


class InMemoryUsers:
    def __init__(self) -> None:
        self._users: Dict[str, Dict[str, str | bytes]] = {}

    def add_user(self, username: str, password: str, role: str) -> None:
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        self._users[username] = {"hash": hashed, "role": role}

    def verify(self, username: str, password: str) -> str | None:
        user = self._users.get(username)
        if user is None:
            return None
        if bcrypt.checkpw(password.encode("utf-8"), user["hash"]):
            return str(user["role"])
        return None


def _demo() -> None:
    rbac = RoleAccessControl()
    store = InMemoryDataStore()
    users = InMemoryUsers()
    
    users.add_user("alice", "Admin123", "Admin")
    users.add_user("bob", "Editor123", "Editor")
    users.add_user("carla", "Usuario123", "Usuario")

    print("Usuarios de prueba:")
    print("- alice / Admin123 (Admin)")
    print("- bob / Editor123 (Editor)")
    print("- carla / Usuario123 (Usuario)")

    username = input("Usuario: ").strip()
    password = input("Contraseña: ").strip()
    role = users.verify(username, password)
    if role is None:
        print("Credenciales invalidas")
        return

    print(f"Rol asignado: {role}")
    actions = {
        "1": "Crear datos",
        "2": "Leer datos",
        "3": "Editar datos",
        "4": "Eliminar datos",
        "0": "Salir",
    }

    while True:
        print("\nAcciones disponibles:")
        print("1) Crear datos")
        print("2) Leer datos")
        print("3) Editar datos")
        print("4) Eliminar datos")
        print("0) Salir")
        action_choice = input("Selecciona una opcion (0-4): ").strip()
        action = actions.get(action_choice)
        if action is None:
            print("Opcion invalida")
            continue
        if action == "Salir":
            break

        auth = rbac.can_access(role, action)
        if not auth.ok:
            print(auth.message)
            continue

        if action == "Leer datos":
            for record in store.list_records():
                print(f"- {record['id']}: {record['contenido']}")
            continue

        if action == "Crear datos":
            content = input("Contenido: ").strip()
            record = store.create_record(content)
            print(f"Creado: {record['id']}: {record['contenido']}")
            continue

        if action == "Editar datos":
            record_id = input("ID a editar: ").strip()
            content = input("Nuevo contenido: ").strip()
            updated = store.update_record(record_id, content)
            print("Actualizado" if updated else "No encontrado")
            continue

        if action == "Eliminar datos":
            record_id = input("ID a eliminar: ").strip()
            deleted = store.delete_record(record_id)
            print("Eliminado" if deleted else "No encontrado")
            continue


if __name__ == "__main__":
    _demo()
