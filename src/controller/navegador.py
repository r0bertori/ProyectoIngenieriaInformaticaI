from PySide6.QtWidgets import QStackedWidget
from view.login_view import LoginView

class Navegador:
    """Gestiona la pila de vistas y la redirección basada en roles."""
    def __init__(self, stacked_widget: QStackedWidget, auth_controller):
        self.stacked_widget = stacked_widget
        self.auth_controller = auth_controller
        self.login_view = None
        self.init_flujo()

    def init_flujo(self):
        # Inicializa la vista de login y conecta la señal de éxito
        self.login_view = LoginView(self.auth_controller)
        self.login_view.login_exitoso.connect(self.redirigir_por_rol)
        
        # Añade la vista al contenedor principal de la aplicación
        self.stacked_widget.addWidget(self.login_view)
        self.stacked_widget.setCurrentWidget(self.login_view)

    def redirigir_por_rol(self, datos_usuario: dict):
        rol = datos_usuario.get("rol", "").lower()
        print(f"[Navegador] Redirigiendo vista para rol: {rol}")

        # Estructura extensible para cargar las vistas de Gerente, Admin, Analista o Emergencias
        if "admin" in rol:
            # self.cargar_vista_administrador(datos_usuario)
            pass
        elif "gerente" in rol:
            # self.cargar_vista_gerente(datos_usuario)
            pass
        elif "emergencia" in rol or "comisaria" in rol or "hospital" in rol:
            # self.cargar_vista_emergencias(datos_usuario)
            pass
        else:
            print("[Navegador] Rol genérico detectado.")