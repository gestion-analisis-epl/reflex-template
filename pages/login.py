import reflex as rx
from states.login_state import LoginState

def login_page() -> rx.Component:
    return rx.center(
        rx.card(
            rx.vstack(
                rx.center(
                    rx.image(
                        src="https://file.garden/aWUUaolUC34GsWOc/logo_kronos.png",
                        width="3em",
                        height="auto",
                        border_radius="25%"
                    ),
                    rx.heading(
                        "Ingresa a tu cuenta",
                        size="6",
                        as_="h2",
                        text_align="center",
                        width="100%",
                    ),
                    direction="column",
                    spacing="5",
                    width="100%",
                ),
                rx.hstack(
                    rx.image(
                        src="https://file.garden/aWUUaolUC34GsWOc/logo_kronos.png"
                    ),
                    direction="column",
                ),
                rx.vstack(
                    rx.text(
                        "Usuario",
                        size="3",
                        weight="medium",
                        text_align="left",
                        width="100%",
                    ),
                    rx.input(
                        rx.input.slot(rx.icon("user")),
                        placeholder="Ingresa tu usuario",
                        type="text",
                        size="3",
                        value=LoginState.username,
                        on_change=LoginState.set_username,
                        width="100%",
                    ),
                    spacing="2",
                    width="100%",
                ),
                rx.vstack(
                    rx.hstack(
                        rx.text("Contraseña", size="3", weight="medium", width="100%"),
                        justify="between",
                        width="100%",
                    ),
                    rx.input(
                        rx.input.slot(rx.icon("lock")),
                        placeholder="Ingresa tu contraseña",
                        type="password",
                        size="3",
                        value=LoginState.password,
                        on_change=LoginState.set_password,
                        width="100%",
                    ),
                    spacing="2",
                    width="100%"
                ),
                rx.button(
                    "Ingresar",
                    size="3",
                    width="100%",
                    loading=LoginState.cargando,
                    on_click=LoginState.validar_login,
                    border_radius="full",
                ),
                spacing="6",
                width="100%",
            ),
            max_width="28em",
            size="4",
            width="100%",
            style = {
                "background": "rgba(255, 255, 255, 0.2)",
                "backdrop-filter": "blur(5px)",
                "-webbit-backdrop-filter": "blur(5px)",
                "border": "1px solid rgba(255, 255, 255, 0.3)",
                "border_radius": "16px",
                "box_shadow": "0 4px 30px rgba(0, 0, 0, 0.1)",
            }
        ),
        height="100vh", 
        background="linear-gradient(45deg, var(--indigo-9), var(--teal-9))",
    )