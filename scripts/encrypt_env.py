"""
scripts/encrypt_env.py
──────────────────────
Script de utilidad para cifrar el archivo .env con Fernet (cryptography).

USO:
  python scripts/encrypt_env.py            → Genera clave nueva y cifra .env
  python scripts/encrypt_env.py --verify   → Verifica que .env.enc se pueda descifrar

Resultado:
  • .env.enc       → Archivo cifrado (este SÍ puede ir al servidor, no al repo Git)
  • KRONOS_MASTER_KEY → La clave maestra se muestra en pantalla UNA SOLA VEZ.
                        Guárdala como variable de entorno del sistema en el VPS.

En el VPS (RackNerd), configura la clave con:
  export KRONOS_MASTER_KEY="<clave>"                    # temporal (sesión actual)
  echo 'export KRONOS_MASTER_KEY="<clave>"' >> ~/.bashrc  # permanente
  # O en el servicio systemd con Environment="KRONOS_MASTER_KEY=<clave>"
"""

import sys
import os
from pathlib import Path

# ── Rutas ──────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT / ".env"
ENC_FILE = ROOT / ".env.enc"
KEY_FILE = ROOT / ".kronos_key"   # SOLO para referencia local, NO subir al repo


def cifrar():
    try:
        from cryptography.fernet import Fernet
    except ImportError:
        print("❌ Instala cryptography primero:  pip install cryptography")
        sys.exit(1)

    if not ENV_FILE.exists():
        print(f"❌ No se encontró el archivo {ENV_FILE}")
        sys.exit(1)

    # Generar clave nueva
    key = Fernet.generate_key()
    fernet = Fernet(key)

    # Leer y cifrar
    plaintext = ENV_FILE.read_bytes()
    encrypted = fernet.encrypt(plaintext)

    # Guardar .env.enc
    ENC_FILE.write_bytes(encrypted)

    # Guardar clave en .kronos_key para referencia LOCAL (¡no subir al repo!)
    KEY_FILE.write_text(key.decode())

    print("=" * 60)
    print("✅  .env cifrado exitosamente → .env.enc")
    print("=" * 60)
    print()
    print("🔑  KRONOS_MASTER_KEY (guárdala en lugar seguro):")
    print()
    print(f"    {key.decode()}")
    print()
    print("📋  Configura en el VPS (RackNerd):")
    print(f'    export KRONOS_MASTER_KEY="{key.decode()}"')
    print()
    print("📋  O en el servicio systemd (/etc/systemd/system/kronos-crm.service):")
    print(f'    Environment="KRONOS_MASTER_KEY={key.decode()}"')
    print()
    print("⚠️   El archivo .kronos_key fue guardado localmente para tu referencia.")
    print("     NUNCA subas .kronos_key ni KRONOS_MASTER_KEY al repositorio Git.")
    print("=" * 60)


def verificar():
    try:
        from cryptography.fernet import Fernet, InvalidToken
    except ImportError:
        print("❌ Instala cryptography primero:  pip install cryptography")
        sys.exit(1)

    master_key = os.environ.get("KRONOS_MASTER_KEY")
    if not master_key and KEY_FILE.exists():
        master_key = KEY_FILE.read_text().strip()
        print(f"ℹ️  Usando clave desde archivo local .kronos_key")

    if not master_key:
        print("❌ No se encontró KRONOS_MASTER_KEY (ni como env var ni en .kronos_key)")
        sys.exit(1)

    if not ENC_FILE.exists():
        print(f"❌ No existe {ENC_FILE}. Ejecuta primero: python scripts/encrypt_env.py")
        sys.exit(1)

    try:
        fernet = Fernet(master_key.encode())
        decrypted = fernet.decrypt(ENC_FILE.read_bytes()).decode("utf-8")
        print("✅  Verificación exitosa. Contenido descifrado:")
        print("-" * 40)
        for line in decrypted.splitlines():
            # Ocultar valores sensibles en la verificación
            if "=" in line and not line.startswith("#"):
                key_name, _, val = line.partition("=")
                hidden = val[:6] + "..." + val[-4:] if len(val) > 12 else "***"
                print(f"  {key_name.strip()} = {hidden}")
            else:
                print(f"  {line}")
        print("-" * 40)
    except InvalidToken:
        print("❌ La clave no coincide con el archivo cifrado")
        sys.exit(1)


if __name__ == "__main__":
    if "--verify" in sys.argv:
        verificar()
    else:
        cifrar()
