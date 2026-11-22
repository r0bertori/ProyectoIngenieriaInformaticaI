import hashlib
import json
import os
from rutas import DATA_DIR

USUARIOS_FILE = DATA_DIR / "usuarios.json"

def _cargar_datos():
    """Carga la lista de usuarios desde data/usuarios.json con persistencia real."""
    if not USUARIOS_FILE.exists():
        guardar_usuarios([])
        return []
    try:
        with open(USUARIOS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def guardar_usuarios(usuarios):
    """Guarda la lista de usuarios en el JSON asegurando indentación de 4 espacios."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(USUARIOS_FILE, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)

def hash_password(password, salt):
    """Genera un hash seguro utilizando PBKDF2."""
    if isinstance(salt, str):
        salt_bytes = bytes.fromhex(salt)
    else:
        salt_bytes = salt
    h = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt_bytes, 100000)
    return h.hex()

def buscar(dni):
    """Busca un usuario por su DNI en el fichero JSON persistente."""
    usuarios = _cargar_datos()
    dni_limpio = dni.strip().upper()
    for u in usuarios:
        if u.get("dni", "").strip().upper() == dni_limpio:
            return u
    return None

def crear_usuario(dni, nombre, apellidos, telefono, password, rol, organizacion):
    """Crea un nuevo usuario y lo persiste en data/usuarios.json formateado."""
    usuarios = _cargar_datos()
    dni_limpio = dni.strip().upper()

    # Comprobar si ya existe el DNI
    for u in usuarios:
        if u.get("dni", "").strip().upper() == dni_limpio:
            raise ValueError("El DNI ya está registrado en el sistema.")

    salt = os.urandom(16).hex()
    password_hash = hash_password(password, salt)

    nuevo_usuario = {
        "dni": dni_limpio,
        "nombre": nombre.strip(),
        "apellidos": apellidos.strip(),
        "telefono": telefono.strip(),
        "salt": salt,
        "password_hash": password_hash,
        "rol": rol,
        "organizacion": organizacion.strip() if organizacion else "",
        "activo": True
    }

    usuarios.append(nuevo_usuario)
    guardar_usuarios(usuarios)
    return nuevo_usuario