import os
from PySide6.QtCore import Signal, QFile
from PySide6.QtUiTools import QUiLoader
from view.base_view import BaseView

class LoginView(BaseView):
    # Señal que emite los datos del usuario autenticado hacia el Navegador
    login_exitoso = Signal(dict)

    def __init__(self, auth_controller):
        super().__init__()
        self.auth_controller = auth_controller
        self.ui = None
        self.init_ui()

    def init_ui(self):
        # Carga dinámica del archivo .ui mediante ruta relativa
        ui_path = os.path.join(os.path.dirname(__file__), "login.ui")
        if os.path.exists(ui_path):
            loader = QUiLoader()
            file = QFile(ui_path)
            file.open(QFile.ReadOnly)
            self.ui = loader.load(file, self)
            file.close()

            # Conexión de eventos de botones definidos en el .ui
            if hasattr(self.ui, "btn_login"):
                self.ui.btn_login.clicked.connect(self.handle_login)
            if hasattr(self.ui, "btn_registrar"):
                self.ui.btn_registrar.clicked.connect(self.handle_register)
        else:
            self.mostrar_error("Error crítico", f"No se encontró la interfaz en: {ui_path}")

    def handle_login(self):
        usuario = self.ui.input_user.text().strip()
        password = self.ui.input_password.text().strip()

        if not usuario or not password:
            self.mostrar_error("Campos vacíos", "Por favor, introduce tu usuario y contraseña.")
            return

        resultado = self.auth_controller.validar_credenciales(usuario, password)
        if resultado:
            self.mostrar_mensaje("Acceso permitido", f"¡Bienvenido de nuevo, {usuario}!")
            self.login_exitoso.emit(resultado)
        else:
            self.mostrar_error("Error de autenticación", "Usuario o contraseña incorrectos.")

    def handle_register(self):
        usuario = self.ui.input_user.text().strip()
        password = self.ui.input_password.text().strip()
        # Rol por defecto asignado en registro rápido o controlado por interfaz
        rol = "Gerente" 

        if not usuario or not password:
            self.mostrar_error("Campos vacíos", "Introduce usuario y contraseña para registrarte.")
            return

        exito = self.auth_controller.registrar_usuario(usuario, password, rol)
        if exito:
            self.mostrar_mensaje("Registro exitoso", "Usuario registrado correctamente. Ya puedes iniciar sesión.")
        else:
            self.mostrar_error("Error de registro", "El usuario ya existe o no se pudo guardar en el sistema.")