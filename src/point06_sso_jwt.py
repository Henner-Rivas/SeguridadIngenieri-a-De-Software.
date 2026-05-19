"""Punto 6: SSO basico con JWT para multiples servicios."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Dict

try:
    import jwt
except ImportError as exc:  # pragma: no cover - runtime guard
    raise SystemExit(
        "Falta instalar dependencia: python3 -m pip install -r requirements.txt"
    ) from exc


JWT_SECRET = "demo_secret_key"
JWT_ALGORITHM = "HS256"
JWT_EXP_MINUTES = 10


@dataclass
class AuthResult:
    ok: bool
    message: str
    token: str | None = None


class InMemoryUsers:
    def __init__(self) -> None:
        self._users: Dict[str, Dict[str, str]] = {
            "admin": {
                "password": "1234",
                "email": "admin@example.com",
                "role": "Admin",
            },
            "maria": {
                "password": "abcd",
                "email": "maria@example.com",
                "role": "Usuario",
            },
        }

    def verify(self, username: str, password: str) -> bool:
        user = self._users.get(username)
        if user is None:
            return False
        return user["password"] == password

    def get_profile(self, username: str) -> Dict[str, str] | None:
        user = self._users.get(username)
        if user is None:
            return None
        return {"email": user["email"], "role": user["role"]}


def generate_token(username: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": username,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=JWT_EXP_MINUTES)).timestamp()),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def validate_token(token: str) -> tuple[bool, str, str | None]:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        return False, "Token expirado", None
    except jwt.InvalidTokenError:
        return False, "Token invalido", None

    return True, "Token valido", str(payload.get("sub"))


def service_a(token: str, users: InMemoryUsers) -> str:
    ok, message, username = validate_token(token)
    if not ok or username is None:
        return f"Servicio A: acceso denegado ({message})"
    profile = users.get_profile(username)
    if profile is None:
        return "Servicio A: usuario no encontrado"
    return f"Servicio A: correo = {profile['email']}"


def service_b(token: str, users: InMemoryUsers) -> str:
    ok, message, username = validate_token(token)
    if not ok or username is None:
        return f"Servicio B: acceso denegado ({message})"
    profile = users.get_profile(username)
    if profile is None:
        return "Servicio B: usuario no encontrado"
    return f"Servicio B: rol = {profile['role']}"


def _demo() -> None:
    users = InMemoryUsers()

    print("Usuarios de prueba:")
    print("- admin / 1234")
    print("- maria / abcd")

    username = input("Usuario: ").strip()
    password = input("Contraseña: ").strip()

    if not users.verify(username, password):
        print("Credenciales invalidas")
        return

    token = generate_token(username)
    print("\nToken generado:")
    print(token)

    print("\nAcceso a servicios con el mismo token:")
    print(service_a(token, users))
    print(service_b(token, users))

    print("\nProbar con token manual (opcional):")
    manual = input("Token (enter para omitir): ").strip()
    if manual:
        print(service_a(manual, users))
        print(service_b(manual, users))


if __name__ == "__main__":
    _demo()
