"""Punto 4: Cifrar y descifrar datos sensibles con AES (simulado)."""

from __future__ import annotations

import base64
import os

try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives.padding import PKCS7
except ImportError as exc:  # pragma: no cover - runtime guard
    raise SystemExit(
        "Falta instalar dependencia: python3 -m pip install -r requirements.txt"
    ) from exc


def _encrypt_aes(plaintext: str, key: bytes, iv: bytes) -> bytes:
    padder = PKCS7(algorithms.AES.block_size).padder()
    padded = padder.update(plaintext.encode("utf-8")) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    return encryptor.update(padded) + encryptor.finalize()


def _decrypt_aes(ciphertext: bytes, key: bytes, iv: bytes) -> str:
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded) + unpadder.finalize()
    return plaintext.decode("utf-8")


def _demo() -> None:
    data = input("Datos sensibles: ").strip()
    if not data:
        print("No se ingresaron datos")
        return

    key = os.urandom(32)  # AES-256
    iv = os.urandom(16)   # 128-bit IV

    ciphertext = _encrypt_aes(data, key, iv)
    encoded = base64.b64encode(iv + ciphertext).decode("ascii")
    print("\nTexto cifrado (base64):")
    print(encoded)

    decoded = base64.b64decode(encoded.encode("ascii"))
    iv_read = decoded[:16]
    cipher_read = decoded[16:]
    decrypted = _decrypt_aes(cipher_read, key, iv_read)
    print("\nTexto descifrado:")
    print(decrypted)


if __name__ == "__main__":
    _demo()
