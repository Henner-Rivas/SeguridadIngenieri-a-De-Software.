# SistemaLoginSeguridad

Resumen del proyecto con las 10 actividades de "Seguridad en Ingenieria de Software", mas instrucciones de ejecucion paso a paso.

## Requisitos

- Python 3.10+ recomendado
- Instalar dependencias:

```bash
python3 -m pip install -r requirements.txt
```

## Puntos y pruebas paso a paso

### Punto 1: Autenticacion basica con bcrypt

Archivo: src/point01_auth_basic.py

Pasos:
1. Ejecuta:
   ```bash
   python3 src/point01_auth_basic.py
   ```
2. Puedes iniciar sesion con el usuario de prueba:
   - Usuario: admin
   - Contrasena: ContrasenaSegura123
3. (Opcional) Registra un usuario nuevo cuando el script lo solicite.

### Punto 2: Deteccion de fuerza bruta y bloqueo

Archivo: src/point02_bruteforce_detection.py

Pasos:
1. Ejecuta:
   ```bash
   python3 src/point02_bruteforce_detection.py
   ```
2. Inicia sesion con:
   - Usuario: admin
   - Contrasena: ContraseñaSegura123
3. Ingresa contrasenas incorrectas 4 veces para bloquear al usuario.
4. Verifica que el usuario bloqueado no puede acceder hasta reiniciar el programa.

### Punto 3: Validacion contra inyeccion SQL (simulada)

Archivo: src/point03_sql_injection_validation.py

Pasos:
1. Ejecuta:
   ```bash
   python3 src/point03_sql_injection_validation.py
   ```
2. Prueba consulta valida:
   ```
   SELECT * FROM usuarios WHERE nombre = 'admin'
   ```
3. Prueba consulta insegura:
   ```
   SELECT * FROM usuarios WHERE nombre = 'admin' OR '1'='1'
   ```

### Punto 4: Cifrado y descifrado con AES

Archivo: src/point04_aes_encrypt_decrypt.py

Pasos:
1. Ejecuta:
   ```bash
   python3 src/point04_aes_encrypt_decrypt.py
   ```
2. Ingresa datos sensibles (ej. 1234-5678-9876-5432).
3. Observa el texto cifrado y luego el texto descifrado.

### Punto 5: Roles y permisos

Archivo: src/point05_roles_permissions.py

Pasos:
1. Ejecuta:
   ```bash
   python3 src/point05_roles_permissions.py
   ```
2. Inicia sesion con:
   - alice / Admin123 (Admin)
   - bob / Editor123 (Editor)
   - carla / Usuario123 (Usuario)
3. Usa el menu numerico para crear/leer/editar/eliminar datos segun permisos.

### Punto 6: SSO basico con JWT

Archivo: src/point06_sso_jwt.py

Pasos:
1. Ejecuta:
   ```bash
   python3 src/point06_sso_jwt.py
   ```
2. Inicia sesion con:
   - admin / 1234
   - maria / abcd
3. El token generado se reutiliza en Servicio A (correo) y Servicio B (rol).

### Punto 7: Auditoria de contrasenas

Archivo: src/point07_password_audit.py

Pasos:
1. Ejecuta:
   ```bash
   python3 src/point07_password_audit.py
   ```
2. Ingresa una lista separada por comas o presiona Enter para usar el ejemplo.
3. Revisa el reporte de contrasenas validas e invalidas.

### Punto 8: GDPR (acceso y borrado)

Archivo: src/point08_gdpr_simulation.py

Pasos:
1. Ejecuta:
   ```bash
   python3 src/point08_gdpr_simulation.py
   ```
2. Inicia sesion con:
   - admin / Admin123
   - maria / Maria123
3. Solicita acceso a datos o elimina datos del usuario.

### Punto 9: Sesion segura en Flask

Archivo: src/point09_flask_secure_session.py

Pasos:
1. Ejecuta:
   ```bash
   python3 src/point09_flask_secure_session.py
   ```
2. Abre:
   - http://127.0.0.1:5000/login
3. Credenciales:
   - admin / 1234
4. La sesion expira por inactividad en 10 minutos.

### Punto 10: Analizador Bandit

Archivo: src/point10_bandit_analysis.py

Pasos:
1. Ejecuta:
   ```bash
   python3 src/point10_bandit_analysis.py
   ```
2. Presiona Enter para escanear "src".
3. Revisa el reporte en la terminal.

## Notas

- Este proyecto es una simulacion educativa.
- Algunos scripts usan datos en memoria y se reinician al cerrar el programa.
