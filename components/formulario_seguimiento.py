import reflex as rx
from states.lead_state import LeadState
from utils.selectboxes import tipo_origen, status_actual, lineas_negocio, tipos_seguimiento

def formulario_seguimiento() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.text("Ejecutivo", size="2", color_scheme="gray", weight="medium"),
            rx.select.root(
                rx.select.trigger(placeholder="Selecciona ejecutivo"),
                rx.select.content(
                    rx.foreach(
                        LeadState.ejecutivos,
                        lambda ejecutivo: rx.select.item(
                            ejecutivo["nombre"],
                            value=ejecutivo["nombre"],
                        ),
                    )
                ),
                value=LeadState.nombre_ejecutivo_seguimiento,
                on_change=LeadState.set_nombre_ejecutivo_seguimiento,
                width="100%",
            ),
            direction="column",
            gap="8px",
            width="100%",
        ),
        rx.flex(
            rx.text("Tipo de seguimiento", size="2", color_scheme="gray", weight="medium"),
            rx.select.root(
                rx.select.trigger(placeholder="Selecciona tipo"),
                rx.select.content(
                    *[rx.select.item(tipo, value=tipo) for tipo in tipos_seguimiento]
                ),
                value=LeadState.tipo_seguimiento,
                on_change=LeadState.set_tipo_seguimiento,
                width="100%",
            ),
            direction="column",
            gap="8px",
            width="100%",
        ),
        rx.flex(
            rx.text("Fecha de seguimiento", size="2", color_scheme="gray", weight="medium"),
            rx.input(
                type="date",
                value=LeadState.fecha_seguimiento,
                on_change=LeadState.set_fecha_seguimiento,
                width="100%",
            ),
            direction="column",
            gap="8px",
            width="100%",
        ),
        rx.flex(
            rx.text("Notas", size="2", color_scheme="gray", weight="medium"),
            rx.text_area(
                placeholder="Describe el seguimiento realizado...",
                value=LeadState.notas_seguimiento,
                on_change=LeadState.set_notas_seguimiento,
                width="100%",
                rows="4",
            ),
            direction="column",
            gap="8px",
            width="100%",
        ),
        rx.flex(
            rx.text("Próximo seguimiento (opcional)", size="2", color_scheme="gray", weight="medium"),
            rx.input(
                type="date",
                value=LeadState.proximo_seguimiento,
                on_change=LeadState.set_proximo_seguimiento,
                width="100%",
            ),
            direction="column",
            gap="8px",
            width="100%",
        ),
        rx.button(
            "Agregar Seguimiento",
            on_click=LeadState.agregar_seguimiento,
            loading=LeadState.cargando,
            width="100%",
        ),
        direction="column",
        gap="16px",
        width="100%",
    )
