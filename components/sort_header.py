import reflex as rx
from states.lead_state import LeadState
from utils.selectboxes import tipo_origen, status_actual, lineas_negocio, tipos_seguimiento

def sort_header(label: str, col: str) -> rx.Component:
    return rx.hstack(
        rx.text(label, size="2", weight="medium"),
        rx.cond(
            LeadState.sort_col == col,
            rx.cond(
                LeadState.sort_asc,
                rx.icon("chevron-up", size=13),
                rx.icon("chevron-down", size=13),
            ),
            rx.icon("chevrons-up-down", size=13, color="var(--gray-8)"),
        ),
        gap="4px",
        align="center",
        cursor="pointer",
        _hover={"opacity": "0.75"},
    )
