import hmac
import json
from model import usuario_model as um
from rutas import DATA_DIR


class AuthController:
    def login(self, dni, password):
        """Devuelve el usuario si las credenciales son correctas; si no, None."""
        usuario = um.buscar(dni.strip().upper())
        if not usuario or not usuario.get("activo", True):
            return None
        esperado = um.hash_password(password, usuario["salt"])
        return usuario if hmac.compare_digest(esperado, usuario["password_hash"]) else None

    def _roles(self):
        roles_file = DATA_DIR / "roles.json"
        if roles_file.exists():
            with open(roles_file, encoding="utf-8") as f:
                return json.load(f).get("roles", [])
        return []

    def vista_para_rol(self, rol):
        """Nombre del .ui al que se redirige cada rol (según data/roles.json)."""
        return next((r["vista"] for r in self._roles() if r["id"] == rol), None)

    def nombre_rol(self, rol):
        return next((r["nombre"] for r in self._roles() if r["id"] == rol), rol)

    def registrar(self, dni, nombre, apellidos, telefono, password, rol, organizacion):
        """Devuelve (ok, mensaje). El rol de administrador no se puede auto-registrar."""
        if rol == "administrador":
            return False, "El rol de administrador solo lo asigna otro administrador."
        try:
            um.crear_usuario(dni, nombre, apellidos, telefono, password, rol, organizacion)
        except ValueError as error:
            return False, str(error)
        except Exception as e:
            return False, f"Error al registrar usuario: {e}"
        return True, "Registro correcto. Ya puedes iniciar sesión."