import sys
from PyQt6 import QtWidgets, uic

# Uso: python main.py [login|gerente|analista|admin|emergencias]
pantalla = sys.argv[1] if len(sys.argv) > 1 else "login"

app = QtWidgets.QApplication(sys.argv)
with open(f"src/views/styles.qss", encoding="utf-8") as f:
    app.setStyleSheet(f.read())

ventana = QtWidgets.QWidget()
uic.loadUi(f"src/views/{pantalla}.ui", ventana)
ventana.show()
sys.exit(app.exec())