"""Punto 7: Auditoria basica de contrasenas con politicas."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class PasswordCheck:
    password: str
    ok: bool
    reasons: List[str]


def audit_password(password: str, min_length: int = 8) -> PasswordCheck:
    reasons: List[str] = []

    if len(password) < min_length:
        reasons.append(f"Longitud minima {min_length}")

    if not any(char.isdigit() for char in password):
        reasons.append("Debe incluir un numero")

    if not any(not char.isalnum() for char in password):
        reasons.append("Debe incluir un caracter especial")

    ok = len(reasons) == 0
    return PasswordCheck(password=password, ok=ok, reasons=reasons)


def _demo() -> None:
    sample = ["1234", "Admin@2023", "password"]
    raw = input(
        "Lista de contrasenas (coma separada, enter para usar ejemplo): "
    ).strip()
    passwords = [p.strip() for p in raw.split(",") if p.strip()] if raw else sample

    print("\nReporte de auditoria:")
    for pwd in passwords:
        result = audit_password(pwd)
        if result.ok:
            print(f"- {pwd}: VALIDA")
        else:
            reasons = ", ".join(result.reasons)
            print(f"- {pwd}: INVALIDA ({reasons})")


if __name__ == "__main__":
    _demo()
