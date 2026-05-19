"""Punto 10: Analizador de codigo con Bandit (simulacion guiada)."""

from __future__ import annotations

import subprocess
from pathlib import Path


def run_bandit(target: str) -> int:
    command = [
        "python3",
        "-m",
        "bandit",
        "-r",
        target,
        "-f",
        "txt",
    ]
    print("Ejecutando:", " ".join(command))
    return subprocess.call(command)


def _demo() -> None:
    print("Analizador Bandit")
    print("Ejemplo de vulnerabilidad: os.system('rm -rf /')")

    target = input("Directorio a escanear (enter para 'src'): ").strip()
    if not target:
        target = "src"

    if not Path(target).exists():
        print("Directorio no encontrado")
        return

    exit_code = run_bandit(target)
    if exit_code == 0:
        print("\nBandit finalizo sin errores de ejecucion.")
        print("Si no hay hallazgos, el reporte aparecera como 'No issues identified'.")
    else:
        print("\nBandit finalizo con codigo de salida:", exit_code)

    print("\nSugerencias de correccion:")
    print("- Evitar os.system; usar subprocess.run con listas y sin shell.")
    print("- Validar y sanitizar entradas externas.")
    print("- Usar rutas seguras y permisos minimos necesarios.")


if __name__ == "__main__":
    _demo()
