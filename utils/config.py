"""
utils/config.py
───────────────
Punto central de configuración de la aplicación.

Flujo de credenciales:
  1. Si existe KRONOS_MASTER_KEY en el entorno del sistema (variable de SO),
     se intenta descifrar el archivo `.env.enc` con Fernet.
  2. Si no existe la clave maestra (entorno de desarrollo local sin cifrado),
     se cae back al `.env` plano con dotenv normal.

Esto permite:
  - En LOCAL → usar `.env` plano (sin cambios al flujo de dev).
  - En PRODUCCIÓN (RackNerd) → usar `.env.enc` cifrado + KRONOS_MASTER_KEY
    como variable de entorno del sistema operativo (no en el repo).
"""

import os
from pathlib import Path

# ── Raíz del proyecto ────────────────────────────────────────────────────────
_BASE_DIR = Path(__file__).resolve().parent.parent
_ENV_FILE = _BASE_DIR / ".env"
_ENV_ENC_FILE = _BASE_DIR / ".env.enc"

# ── Intento 1: Cifrado con Fernet ────────────────────────────────────────────
_master_key = os.environ.get("KRONOS_MASTER_KEY")

if _master_key and _ENV_ENC_FILE.exists():
    try:
        from cryptography.fernet import Fernet, InvalidToken
        _fernet = Fernet(_master_key.encode())
        _decrypted = _fernet.decrypt(_ENV_ENC_FILE.read_bytes()).decode("utf-8")

        # Parsear el contenido descifrado línea a línea (formato KEY=VALUE)
        for _line in _decrypted.splitlines():
            _line = _line.strip()
            if not _line or _line.startswith("#"):
                continue
            if "=" in _line:
                _key, _, _val = _line.partition("=")
                # Quitar comillas opcionales
                _val = _val.strip().strip('"').strip("'")
                os.environ.setdefault(_key.strip(), _val)

        print("[config] ✅ Variables cargadas desde .env.enc (cifrado Fernet)")

    except ImportError:
        print("[config] ⚠️  cryptography no instalado — usando .env plano")
        from dotenv import load_dotenv
        load_dotenv(_ENV_FILE)

    except Exception as e:
        print(f"[config] ❌ Error al descifrar .env.enc: {e} — usando .env plano")
        from dotenv import load_dotenv
        load_dotenv(_ENV_FILE)

# ── Intento 2: .env plano (desarrollo local) ─────────────────────────────────
else:
    from dotenv import load_dotenv
    load_dotenv(_ENV_FILE)
    if not _master_key:
        print("[config] 🔓 Modo desarrollo: usando .env plano (KRONOS_MASTER_KEY no definida)")

# ── Variables exportadas ─────────────────────────────────────────────────────
DATABASE_URL: str = os.getenv("DATABASE_URL", "")
DB_URL: str = os.getenv("db_url", DATABASE_URL)  # alias para connection_db

if not DATABASE_URL:
    print("[config] ⚠️  DATABASE_URL no encontrada en ninguna fuente de configuración")
