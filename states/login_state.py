import reflex as rx

from repository.users_repository import UsersRepository
from utils.config import DATABASE_URL


class LoginState(rx.State):
    username: str = ""
    password: str = ""
    cargando: bool = False
    is_authenticated: bool = False
    user_role: str = ""

    def set_username(self, value: str):
        self.username = value

    def set_password(self, value: str):
        self.password = value

    def require_auth(self):
        if not self.is_authenticated:
            return rx.redirect("/login")

    def redirect_if_authenticated(self):
        if self.is_authenticated:
            return rx.redirect("/")

    def logout(self):
        self.is_authenticated = False
        self.username = ""
        self.password = ""
        self.user_role = ""
        yield rx.toast.info("Sesión cerrada")
        yield rx.redirect("/login")

    def validar_login(self):
        username = (self.username or "").strip()
        password = self.password or ""

        if not username or not password:
            yield rx.toast.warning("Ingresa usuario y contraseña")
            return

        self.cargando = True
        try:
            repo = UsersRepository(DATABASE_URL)

            usuario_valido = repo.validar_credenciales(username, password)
            if usuario_valido:
                self.is_authenticated = True
                self.username = usuario_valido.get("username", username)
                self.user_role = usuario_valido.get("role", "")
                self.password = ""
                yield rx.toast.success(f"Bienvenido, {self.username}")
                yield rx.redirect("/")
                return

            usuario_encontrado = repo.obtener_usuario_por_username(username)
            if usuario_encontrado:
                yield rx.toast.error("Contraseña inválida")
            else:
                yield rx.toast.warning("Usuario no encontrado")
        except Exception as e:
            yield rx.toast.error(f"Error al validar login: {str(e)}")
        finally:
            self.cargando = False
