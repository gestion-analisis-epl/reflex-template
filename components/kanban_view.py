import reflex as rx
from states.lead_state import LeadState

# Configuración de columnas Kanban con colores y metadatos
# Usa los status de selectboxes.py
KANBAN_COLUMNS = [
    {"status": "INTERESADO",            "color": "blue",   "icon": "user-search"},
    {"status": "DETECCION DE NECESIDAD", "color": "cyan",   "icon": "search"},
    {"status": "SEGUIMIENTO",           "color": "amber",  "icon": "clock"},
    {"status": "PROVEEDOR",             "color": "purple", "icon": "handshake"},
    {"status": "GANADO",                "color": "green",  "icon": "trophy"},
    {"status": "PROYECTO PAUSADO",      "color": "gray",   "icon": "pause"},
    {"status": "DECLINADO",             "color": "orange", "icon": "circle-x"},
    {"status": "CANCELADO",             "color": "red",    "icon": "ban"},
]

# Mapea color_scheme → clase CSS inline para el borde superior de la tarjeta
BORDER_COLOR_MAP = {
    "blue":   "#3b82f6",
    "cyan":   "#06b6d4",
    "amber":  "#f59e0b",
    "orange": "#f97316",
    "green":  "#22c55e",
    "red":    "#ef4444",
    "gray":   "#6b7280",
    "purple": "#a855f7",
}


def kanban_card(lead: dict) -> rx.Component:
    """Tarjeta individual dentro de una columna Kanban."""
    return rx.card(
        rx.vstack(
            # Cabecera: ID + Acciones
            rx.hstack(
                rx.badge(
                    lead["id_interno"],
                    variant="soft",
                    color_scheme="gray",
                    size="1",
                    font_family="monospace",
                ),
                rx.spacer(),
                rx.hstack(
                    rx.icon_button(
                        rx.icon("eye", size=12),
                        size="1",
                        variant="ghost",
                        color_scheme="blue",
                        on_click=lambda: LeadState.abrir_dialog_ver(lead["id_lead"]),
                        cursor="pointer",
                    ),
                    rx.icon_button(
                        rx.icon("pencil", size=12),
                        size="1",
                        variant="ghost",
                        color_scheme="amber",
                        on_click=lambda: LeadState.abrir_dialog_editar(lead["id_lead"]),
                        cursor="pointer",
                    ),
                    gap="4px",
                ),
                width="100%",
                align="center",
            ),
            # Nombre cliente
            rx.text(
                lead["nombre_cliente"],
                size="2",
                weight="bold",
                trim="both",
            ),
            # Ejecutivo
            rx.hstack(
                rx.icon("user", size=11, color="var(--gray-9)"),
                rx.text(lead["nombre_ejecutivo"], size="1", color_scheme="gray"),
                gap="4px",
                align="center",
            ),
            # Monto
            rx.hstack(
                rx.icon("circle-dollar-sign", size=11, color="var(--green-9)"),
                rx.text(lead["monto_formateado"], size="1", weight="medium", color_scheme="green"),
                gap="4px",
                align="center",
            ),
            # Ciudad + Cierre estimado
            rx.hstack(
                rx.hstack(
                    rx.icon("map-pin", size=11, color="var(--gray-9)"),
                    rx.text(lead["ciudad_interes"], size="1", color_scheme="gray"),
                    gap="4px",
                    align="center",
                ),
                rx.spacer(),
                rx.hstack(
                    rx.icon("calendar", size=11, color="var(--gray-9)"),
                    rx.text(lead["fecha_estimada_cierre"], size="1", color_scheme="gray"),
                    gap="4px",
                    align="center",
                ),
                width="100%",
            ),
            # Selector de status para mover entre columnas
            rx.divider(margin_y="4px"),
            rx.hstack(
                rx.icon("move", size=11, color="var(--gray-9)"),
                rx.select.root(
                    rx.select.trigger(
                        placeholder="Mover a...",
                        size="1",
                    ),
                    rx.select.content(
                        *[
                            rx.select.item(col["status"], value=col["status"])
                            for col in KANBAN_COLUMNS
                        ]
                    ),
                    value=lead["status_actual"],
                    on_change=lambda nuevo_status: LeadState.actualizar_status_lead(lead["id_lead"], nuevo_status),
                    size="1",
                    width="100%",
                ),
                gap="4px",
                align="center",
                width="100%",
            ),
            gap="8px",
            width="100%",
            align="start",
        ),
        width="100%",
        style={
            "cursor": "default",
            "transition": "box-shadow 0.15s ease, transform 0.15s ease",
            "_hover": {
                "box-shadow": "0 4px 16px rgba(0,0,0,0.12)",
                "transform": "translateY(-2px)",
            },
        },
    )


def kanban_column(col_cfg: dict) -> rx.Component:
    """Columna del tablero Kanban para un status determinado."""
    status   = col_cfg["status"]
    color    = col_cfg["color"]
    icon_name = col_cfg["icon"]
    border_top_color = BORDER_COLOR_MAP.get(color, "#6b7280")

    return rx.box(
        rx.vstack(
            # Encabezado de columna
            rx.hstack(
                rx.box(
                    rx.icon(icon_name, size=14),
                    color=f"var(--{color}-11)",
                ),
                rx.text(status, size="2", weight="bold"),
                rx.spacer(),
                rx.badge(
                    LeadState.conteo_por_status.get(status, 0),
                    variant="soft",
                    color_scheme=color,
                    size="1",
                ),
                width="100%",
                align="center",
                padding_x="4px",
            ),
            rx.divider(margin_y="4px"),
            # Tarjetas - filtra con rx.cond para evitar problemas con vars
            rx.scroll_area(
                rx.vstack(
                    rx.foreach(
                        LeadState.leads_filtrados,
                        lambda lead: rx.cond(
                            lead["status_actual"] == status,
                            kanban_card(lead),
                            rx.fragment(),
                        ),
                    ),
                    gap="10px",
                    width="100%",
                    min_height="200px",
                    padding_bottom="8px",
                ),
                type="auto",
                scrollbars="vertical",
                style={"max_height": "calc(100vh - 260px)"},
            ),
            gap="0",
            width="100%",
        ),
        background="var(--gray-2)",
        border_radius="12px",
        border=f"1px solid var(--gray-5)",
        border_top=f"3px solid {border_top_color}",
        padding="12px",
        min_width="260px",
        width="260px",
        flex_shrink="0",
    )


def kanban_view() -> rx.Component:
    """Vista Kanban completa — drop-in replacement para la tabla de leads."""
    return rx.box(
        rx.hstack(
            *[kanban_column(col) for col in KANBAN_COLUMNS],
            gap="14px",
            align="start",
            width="max-content",
            padding_bottom="12px",
        ),
        overflow_x="auto",
        width="100%",
        padding_y="8px",
    )