"""Punto 1: Sistema de autenticacion basico con hashing bcrypt."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

try:
    import bcrypt
except ImportError as exc:  # pragma: no cover - runtime guard
    raise SystemExit(
        "Falta instalar dependencia: pip install -r requirements.txt"
    ) from exc


@dataclass
class AuthResult:
    ok: bool
    message: str


class InMemoryAuth:
    def __init__(self) -> None:
        self._users: Dict[str, bytes] = {}

    def register_user(self, username: str, password: str) -> AuthResult:
        if not username or not password:
            return AuthResult(False, "Usuario y contrasena son obligatorios")
        if username in self._users:
            return AuthResult(False, "El usuario ya existe")

        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        self._users[username] = hashed
        return AuthResult(True, "Registro exitoso")

    def authenticate(self, username: str, password: str) -> AuthResult:
        if username not in self._users:
            return AuthResult(False, "Credenciales invalidas")

        hashed = self._users[username]
        if bcrypt.checkpw(password.encode("utf-8"), hashed):
            return AuthResult(True, "Inicio de sesion exitoso")
        return AuthResult(False, "Credenciales invalidas")


def _demo() -> None:
    auth = InMemoryAuth()
    auth.register_user("admin", "ContrasenaSegura123")

    print("Usuario de prueba: admin / ContrasenaSegura123")
    print("\nRealizar registro")
    reg_user = input("Usuario: ").strip()
    reg_pass = input("Contrasena: ").strip()
    if reg_user and reg_pass:
        reg_result = auth.register_user(reg_user, reg_pass)
        print(reg_result.message)
    else:
        print("Registro omitido")

    print("\nInicio de sesion")
    login_user = input("Usuario: ").strip()
    login_pass = input("Contrasena: ").strip()
    login_result = auth.authenticate(login_user, login_pass)
    print(login_result.message)


if __name__ == "__main__":
    _demo()
