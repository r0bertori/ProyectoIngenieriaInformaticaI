"""Gestión de usuarios y auditoría de los JSON. Autor: Rodrigo | Historia: [Vista - Administrador]"""
import json
from datetime import datetime

from PyQt6.QtWidgets import QTableWidgetItem

from model import usuario_model as um
from rutas import DATA_DIR

CAMPOS = ("dni", "nombre", "apellidos", "telefono", "rol", "organizacion")


class AdminController:
    def __init__(self, vista, usuario, nombre_rol):
        self.vista = vista
        self.usuario = usuario
        vista.set_usuario(f"{usuario['nombre']} {usuario['apellidos']}", nombre_rol)
        for texto, rol, organizacion in um.PERFILES:
            vista.cmbRol.addItem(texto, (rol, organizacion))
        vista.btnAltaUsuario.clicked.connect(self.alta)
        vista.btnBajaUsuario.clicked.connect(self.baja)
        vista.btnCambiarRol.clicked.connect(self.cambiar_rol)
        vista.btnActualizar.clicked.connect(self.refrescar)
        self.refrescar()

    # ---- utilidades ----
    def _mensaje(self, texto, ok=True):
        color = "#3FB68B" if ok else "#E5574F"
        self.vista.lblMensajeAdmin.setStyleSheet(f"color: {color};")
        self.vista.lblMensajeAdmin.setText(texto)

    def _dni_seleccionado(self):
        fila = self.vista.tblUsuarios.currentRow()
        return None if fila < 0 else self.vista.tblUsuarios.item(fila, 0).text()

    # ---- acciones ----
    def alta(self):
        v = self.vista
        rol, organizacion = v.cmbRol.currentData()
        try:
            um.crear_usuario(v.txtDni.text(), v.txtNombre.text(), v.txtApellidos.text(),
                             v.txtTelefono.text(), v.txtPassword.text(), rol, organizacion)
        except ValueError as error:
            return self._mensaje(str(error), ok=False)
        for campo in (v.txtDni, v.txtNombre, v.txtApellidos, v.txtTelefono, v.txtPassword):
            campo.clear()
        self.refrescar()
        self._mensaje("Usuario creado.")

    def baja(self):
        dni = self._dni_seleccionado()
        if not dni:
            return self._mensaje("Selecciona un usuario de la tabla.", ok=False)
        if dni == self.usuario["dni"]:
            return self._mensaje("No puedes darte de baja a ti mismo.", ok=False)
        try:
            um.eliminar_usuario(dni)
        except ValueError as error:
            return self._mensaje(str(error), ok=False)
        self.refrescar()
        self._mensaje("Usuario eliminado.")

    def cambiar_rol(self):
        dni = self._dni_seleccionado()
        if not dni:
            return self._mensaje("Selecciona un usuario de la tabla.", ok=False)
        if dni == self.usuario["dni"]:
            return self._mensaje("No puedes cambiar tu propio rol.", ok=False)
        rol, organizacion = self.vista.cmbRol.currentData()
        try:
            um.cambiar_rol(dni, rol, organizacion)
        except ValueError as error:
            return self._mensaje(str(error), ok=False)
        self.refrescar()
        self._mensaje("Rol actualizado.")

    # ---- datos en pantalla ----
    def refrescar(self):
        usuarios = um.cargar_usuarios()
        tabla = self.vista.tblUsuarios
        tabla.setRowCount(len(usuarios))
        for fila, u in enumerate(usuarios):
            for col, campo in enumerate(CAMPOS):
                tabla.setItem(fila, col, QTableWidgetItem(str(u[campo])))
        self.vista.txtAuditoria.setPlainText(self.auditar())

    def auditar(self):
        """Resumen de cada fichero de data/: tamaño, última modificación y si el JSON es válido."""
        lineas = []
        for ruta in sorted(DATA_DIR.glob("*.json")):
            try:
                with open(ruta, encoding="utf-8") as f:
                    json.load(f)
                estado = "válido"
            except (OSError, ValueError):
                estado = "ERROR: JSON no válido"
            modificado = datetime.fromtimestamp(ruta.stat().st_mtime).strftime("%d/%m/%Y %H:%M")
            lineas.append(f"{ruta.name:<16} {ruta.stat().st_size:>7} B   {modificado}   {estado}")
        return "\n".join(lineas)
