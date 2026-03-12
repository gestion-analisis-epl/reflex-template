import reflex as rx
from states.lead_state import LeadState
from utils.selectboxes import tipo_origen, status_actual, lineas_negocio, tipos_seguimiento

def tarjeta_seguimiento(seguimiento: dict) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.badge(seguimiento["tipo_seguimiento"], variant="soft", color_scheme="blue"),
                rx.spacer(),
                rx.cond(
                    seguimiento["fecha_creacion"],
                    rx.text(
                        seguimiento["fecha_creacion"].to(str).split("T")[0],
                        size="1",
                        color_scheme="gray",
                    ),
                    rx.text("—", size="1", color_scheme="gray"),
                ),
                width="100%",
            ),
            rx.text(seguimiento["notas"], size="2"),
            rx.hstack(
                rx.text(seguimiento["nombre_ejecutivo"], size="1", color_scheme="gray"),
                rx.cond(
                    seguimiento["proximo_seguimiento"],
                    rx.text(
                        seguimiento["proximo_seguimiento"].to(str).split("T")[0],
                        size="1",
                        color_scheme="gray",
                    ),
                ),
                width="100%",
                gap="8px",
            ),
            align="start",
            width="100%",
            gap="8px",
        ),
        width="100%",
    )

