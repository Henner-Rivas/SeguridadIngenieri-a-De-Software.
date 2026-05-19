"""Punto 2: Deteccion de intentos de fuerza bruta con bloqueo temporal."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List

try:
    import bcrypt
except ImportError as exc:  # pragma: no cover - runtime guard
    raise SystemExit(
        "Falta instalar dependencia: python3 -m pip install -r requirements.txt"
    ) from exc


@dataclass
class LoginEvent:
    timestamp: datetime
    success: bool
    reason: str


class BruteForceGuard:
    def __init__(self, max_failures: int = 3, window_minutes: int = 5) -> None:
        self._max_failures = max_failures
        self._window = timedelta(minutes=window_minutes)
        self._failed_attempts: Dict[str, List[datetime]] = {}
        self._blocked_users: Dict[str, bool] = {}
        self._events: Dict[str, List[LoginEvent]] = {}

    def _record_event(self, username: str, success: bool, reason: str) -> None:
        self._events.setdefault(username, []).append(
            LoginEvent(timestamp=datetime.now(), success=success, reason=reason)
        )

    def _prune_old_failures(self, username: str, now: datetime) -> None:
        cutoff = now - self._window
        failures = self._failed_attempts.get(username, [])
        self._failed_attempts[username] = [t for t in failures if t >= cutoff]

    def is_blocked(self, username: str) -> bool:
        return self._blocked_users.get(username, False)

    def register_attempt(self, username: str, success: bool) -> str:
        now = datetime.now()
        if self.is_blocked(username):
            self._record_event(username, False, "Cuenta bloqueada")
            return "Cuenta bloqueada temporalmente"

        if success:
            self._record_event(username, True, "Inicio de sesion exitoso")
            self._failed_attempts.pop(username, None)
            return "Inicio de sesion exitoso"

        self._prune_old_failures(username, now)
        failures = self._failed_attempts.setdefault(username, [])
        failures.append(now)

        if len(failures) > self._max_failures:
            self._blocked_users[username] = True
            self._record_event(username, False, "Bloqueo por fuerza bruta")
            return "Cuenta bloqueada temporalmente"

        self._record_event(username, False, "Credenciales invalidas")
        remaining = self._max_failures - len(failures) + 1
        return f"Credenciales invalidas (intentos restantes: {remaining})"

    def get_events(self, username: str) -> List[LoginEvent]:
        return list(self._events.get(username, []))


class InMemoryUsers:
    def __init__(self) -> None:
        self._users: Dict[str, bytes] = {}

    def register(self, username: str, password: str) -> str:
        if not username or not password:
            return "Usuario y contrasena son obligatorios"
        if username in self._users:
            return "El usuario ya existe"

        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        self._users[username] = hashed
        return "Registro exitoso"

    def verify(self, username: str, password: str) -> bool:
        hashed = self._users.get(username)
        if hashed is None:
            return False
        return bcrypt.checkpw(password.encode("utf-8"), hashed)


def _demo() -> None:
    guard = BruteForceGuard(max_failures=3, window_minutes=5)
    users = InMemoryUsers()
    users.register("admin", "ContraseñaSegura123")

    print("Usuario de prueba: admin / ContraseñaSegura123")
    print("\nRegistro (opcional)")
    reg_user = input("Usuario: ").strip()
    reg_pass = input("Contraseña: ").strip()
    if reg_user and reg_pass:
        print(users.register(reg_user, reg_pass))
    else:
        print("Registro omitido")

    print("\nInicio de sesion")
    attempt = 1

    while True:
        username = input(f"Usuario (intento {attempt}, q para salir): ").strip()
        if username.lower() == "q":
            break
        password = input("Contraseña: ").strip()
        if password.lower() == "q":
            break

        success = users.verify(username, password)
        message = guard.register_attempt(username, success=success)
        print(message)
        attempt += 1

    print("\nEventos registrados:")
    for event in guard.get_events(username):
        status = "OK" if event.success else "FAIL"
        print(f"- {event.timestamp.isoformat()} [{status}] {event.reason}")


if __name__ == "__main__":
    _demo()
