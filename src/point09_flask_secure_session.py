"""Punto 9: Sesion segura en Flask con expiracion y cookies seguras."""

from __future__ import annotations

from datetime import timedelta
import os

try:
    from flask import Flask, redirect, render_template_string, request, session, url_for
except ImportError as exc:  # pragma: no cover - runtime guard
    raise SystemExit(
        "Falta instalar dependencia: python3 -m pip install -r requirements.txt"
    ) from exc


app = Flask(__name__)
app.secret_key = "demo_secret_key"
use_secure_cookies = os.getenv("FLASK_SECURE_COOKIES", "0") == "1"
app.config.update(
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=10),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=use_secure_cookies,
    SESSION_COOKIE_SAMESITE="Lax",
    TRUSTED_HOSTS=["127.0.0.1", "localhost", "127.0.0.1:5000", "localhost:5000"],
    SERVER_NAME="127.0.0.1:5000",
)

USERS = {"admin": "1234"}

LOGIN_TEMPLATE = """
<!doctype html>
<title>Login</title>
<style>
    body { font-family: "Trebuchet MS", Verdana, sans-serif; background: #f7f7fb; color: #222; }
    .card { max-width: 420px; margin: 48px auto; background: #fff; padding: 24px; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.08); }
    h2 { margin: 0 0 12px; }
    label { display: block; margin: 12px 0 6px; font-weight: 600; }
    input { width: 100%; padding: 10px 12px; border: 1px solid #ddd; border-radius: 8px; }
    button { margin-top: 14px; width: 100%; padding: 10px 12px; background: #1f6feb; color: #fff; border: 0; border-radius: 8px; cursor: pointer; }
    .message { margin-top: 12px; color: #b42318; }
</style>
<div class="card">
    <h2>Iniciar sesion</h2>
    <form method="post">
        <label>Usuario</label>
        <input name="username" />
        <label>Contrasena</label>
        <input name="password" type="password" />
        <button type="submit">Entrar</button>
    </form>
    <p class="message">{{ message }}</p>
</div>
"""

HOME_TEMPLATE = """
<!doctype html>
<title>Inicio</title>
<style>
    body { font-family: "Trebuchet MS", Verdana, sans-serif; background: #f7f7fb; color: #222; }
    .card { max-width: 520px; margin: 48px auto; background: #fff; padding: 24px; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.08); }
    h2 { margin: 0 0 10px; }
    .badge { display: inline-block; padding: 4px 10px; background: #e6f4ff; color: #0958d9; border-radius: 999px; font-size: 12px; }
    a { color: #1f6feb; text-decoration: none; }
</style>
<div class="card">
    <span class="badge">Sesion segura</span>
    <h2>Bienvenido, {{ username }}</h2>
    <p>Sesion activa. Expira por inactividad en 10 minutos.</p>
    <p><a href="{{ url_for('logout') }}">Cerrar sesion</a></p>
</div>
"""


@app.route("/", methods=["GET"])
def index() -> str:
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template_string(HOME_TEMPLATE, username=session["user"])


@app.route("/health", methods=["GET"])
def health() -> str:
    return "OK"


@app.route("/login", methods=["GET", "POST"])
def login() -> str:
    message = ""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if USERS.get(username) == password:
            session.clear()
            session.permanent = True
            session["user"] = username
            return redirect(url_for("index"))
        message = "Credenciales invalidas"
    return render_template_string(LOGIN_TEMPLATE, message=message)


@app.route("/logout", methods=["GET"])
def logout() -> str:
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
