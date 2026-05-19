"""Punto 8: Simulacion de derechos GDPR (acceso y borrado)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class UserData:
    nombre: str
    email: str
    telefono: str
    direccion: str


class InMemoryGdprStore:
    def __init__(self) -> None:
        self._users: Dict[str, UserData] = {
            "admin": UserData(
                nombre="Admin",
                email="admin@example.com",
                telefono="555-0101",
                direccion="Calle Principal 123",
            ),
            "maria": UserData(
                nombre="Maria",
                email="maria@example.com",
                telefono="555-0202",
                direccion="Avenida Central 45",
            ),
        }
        self._passwords: Dict[str, str] = {
            "admin": "Admin123",
            "maria": "Maria123",
        }
        self._audit_log: List[str] = []

    def verify(self, username: str, password: str) -> bool:
        return self._passwords.get(username) == password

    def request_access(self, username: str) -> UserData | None:
        user = self._users.get(username)
        if user is None:
            self._audit_log.append(f"ACCESO FALLIDO: {username}")
            return None
        self._audit_log.append(f"ACCESO CONCEDIDO: {username}")
        return user

    def delete_user(self, username: str) -> bool:
        if username not in self._users:
            self._audit_log.append(f"BORRADO FALLIDO: {username}")
            return False
        self._users.pop(username, None)
        self._audit_log.append(f"BORRADO EXITOSO: {username}")
        return True

    def audit_log(self) -> List[str]:
        return list(self._audit_log)


def _demo() -> None:
    store = InMemoryGdprStore()

    print("Usuarios de prueba: admin, maria")
    username = input("Usuario: ").strip()
    password = input("Contrasena: ").strip()
    if not store.verify(username, password):
        print("Credenciales invalidas")
        return

    print("\nSolicitudes disponibles:")
    print("1) Acceder a mis datos")
    print("2) Eliminar mis datos")
    choice = input("Selecciona una opcion (1-2): ").strip()

    if choice == "1":
        data = store.request_access(username)
        if data is None:
            print("No se encontraron datos del usuario")
        else:
            print("\nDatos personales:")
            print(f"- Nombre: {data.nombre}")
            print(f"- Email: {data.email}")
            print(f"- Telefono: {data.telefono}")
            print(f"- Direccion: {data.direccion}")
    elif choice == "2":
        deleted = store.delete_user(username)
        if deleted:
            print("Datos eliminados completamente")
        else:
            print("No se encontraron datos para eliminar")
    else:
        print("Opcion invalida")

    print("\nRegistro de auditoria:")
    for entry in store.audit_log():
        print(f"- {entry}")


if __name__ == "__main__":
    _demo()
