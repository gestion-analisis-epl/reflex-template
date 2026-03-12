import reflex as rx
from states.lead_state import LeadState
from utils.selectboxes import tipo_origen, status_actual, lineas_negocio, tipos_seguimiento

def badge_status(status_actual: str, color_scheme: str) -> rx.Component:
    return rx.badge(status_actual, variant="soft", align="center", color_scheme=color_scheme, radius="large")

def fila_lead(lead: dict) -> rx.Component:
    return rx.table.row(
        rx.table.cell(lead["id_interno"]),
        rx.table.cell(
            rx.hstack(
                rx.text(lead["nombre_cliente"]),
                rx.text(lead["apellido_cliente"]),
                gap="4px",
            )
        ),
        rx.table.cell(lead["nombre_ejecutivo"]),
        rx.table.cell(
            rx.cond(
                lead["fecha_contacto"],
                lead["fecha_contacto"].to(str)[:10],
                "—",
            )
        ),
        rx.table.cell(
            rx.match(
                lead["tipo_origen"],
                ("DIRECTO", badge_status("DIRECTO", "sky")),
                ("LICITACIÓN", badge_status("LICITACIÓN", "blue")),
                ("REFERIDO", badge_status("REFERIDO", "indigo")),
                ("SITIO WEB", badge_status("SITIO WEB", "mint")),
                ("WHATSAPP", badge_status("WHATSAPP", "grass")),
            ),
        ),
        rx.table.cell(lead["ciudad_interes"]),
        rx.table.cell(lead["servicio_producto_interes"]),
        rx.table.cell(
            rx.match(
                lead["status_actual"],
                ("CANCELADO", badge_status("CANCELADO", "tomato")),
                ("DECLINADO", badge_status("DECLINADO", "red")),
                ("DETECCION DE NECESIDAD", badge_status("DETECCION DE NECESIDAD", "cyan")),
                ("GANADO", badge_status("GANADO", "grass")),
                ("INTERESADO", badge_status("INTERESADO", "blue")),
                ("PROVEEDOR", badge_status("PROVEEDOR", "gray")),
                ("PROYECTO PAUSADO", badge_status("PROYECTO PAUSADO", "amber")),
                ("SEGUIMIENTO", badge_status("SEGUIMIENTO", "sky")),
            ),
        ),
        rx.table.cell(lead["monto_formateado"]),
        rx.table.cell(
            rx.cond(
                lead["fecha_estimada_cierre"],
                lead["fecha_estimada_cierre"].to(str).split("T")[0],
                "—",
            )
        ),
        rx.table.cell(
            rx.cond(
                lead.get("linea_negocio"),
                ", ".join(lead["linea_negocio"]) if isinstance(lead.get("linea_negocio"), list) else lead.get("linea_negocio", "—"),
                "—",
            )
        ),
        rx.table.cell(
            rx.hstack(
                rx.button(
                    rx.icon("eye", size=16),
                    variant="soft",
                    color_scheme="green",
                    size="1",
                    on_click=lambda: LeadState.abrir_dialog_ver(lead["id_lead"]),
                ),
                rx.button(
                    rx.icon("pencil", size=16),
                    variant="soft",
                    color_scheme="blue",
                    size="1",
                    on_click=lambda: LeadState.abrir_dialog_editar(lead["id_lead"]),
                ),
                rx.button(
                    rx.icon("trash-2", size=16),
                    variant="soft",
                    color_scheme="red",
                    size="1",
                    on_click=lambda: LeadState.abrir_dialog_eliminar(lead["id_lead"]),
                ),
                gap="8px",
            )
        ),
    )