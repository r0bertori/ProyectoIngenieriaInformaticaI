import sys
from pathlib import Path
from PyQt6 import QtWidgets, uic

# Carpeta de las vistas: funciona estando main.py en src/ o en la raíz del proyecto.
BASE = Path(__file__).resolve().parent
VISTAS = BASE / "views" if (BASE / "views").exists() else BASE / "src" / "views"

# Pantallas de la demo (usuario escrito en el login -> pantalla que se abre)
PANTALLAS = ("admin", "gerente", "analista", "emergencias")

app = QtWidgets.QApplication(sys.argv)
app.setStyleSheet((VISTAS / "styles.qss").read_text(encoding="utf-8"))

ventanas = {}  # guarda la ventana abierta para que Python no la borre


def mostrar(nombre):
    """Abre la pantalla indicada y cierra la anterior."""
    nueva = QtWidgets.QWidget()
    uic.loadUi(str(VISTAS / f"{nombre}.ui"), nueva)

    if nombre == "login":
        nueva.btnEntrar.clicked.connect(entrar)
    elif hasattr(nueva, "btnCerrarSesion"):
        nueva.btnCerrarSesion.clicked.connect(lambda: mostrar("login"))

    anterior = ventanas.get("actual")
    ventanas["actual"] = nueva
    nueva.show()
    if anterior:
        anterior.close()


def entrar():
    """DEMO: sustituir por la validación real con el JSON y el rol (Roberto)."""
    login = ventanas["actual"]
    usuario = login.txtLoginUsuario.text().strip().lower()
    if usuario in PANTALLAS and (VISTAS / f"{usuario}.ui").exists():
        mostrar(usuario)
    else:
        login.lblErrorLogin.setText("Demo: escribe admin o gerente")


# Uso: python main.py [login|gerente|admin|analista|emergencias]
mostrar(sys.argv[1] if len(sys.argv) > 1 else "login")
sys.exit(app.exec())