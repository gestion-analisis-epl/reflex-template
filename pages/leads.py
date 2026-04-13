import reflex as rx
from states.lead_state import LeadState
from utils.selectboxes import tipo_origen, status_actual, lineas_negocio, tipos_seguimiento
from components.sidebar import sidebar_top_profile
from components.tarjeta_seguimiento import tarjeta_seguimiento
from components.formulario_seguimiento import formulario_seguimiento
from components.sort_header import sort_header
from components.fila_lead import fila_lead
from components.resizable_column import init_resizable_columns
from components.paginacion import paginacion
from components.kanban_view import kanban_view

def badge_status(status_actual: str, color_scheme: str) -> rx.Component:
    return rx.badge(status_actual, variant="soft", align="center", color_scheme=color_scheme, radius="large")

def formulario_lead() -> rx.Component:
    return rx.flex(
        # Fila 1 — Cliente / Ejecutivo
        rx.flex(
            rx.flex(
                rx.text("Cliente", size="2", color_scheme="gray", weight="medium"),
                rx.select.root(
                    rx.select.trigger(placeholder="Selecciona cliente"),
                    rx.select.content(
                        rx.foreach(
                            LeadState.clientes,
                            lambda op: rx.select.item(op["nombre"], value=op["nombre"]),
                        )
                    ),
                    value=LeadState.nombre_cliente,
                    on_change=LeadState.set_nombre_cliente,
                    width="100%",
                ),
                direction="column",
                gap="8px",
                width="100%",
            ),
            rx.flex(
                rx.text("Ejecutivo", size="2", color_scheme="gray", weight="medium"),
                rx.select.root(
                    rx.select.trigger(placeholder="Selecciona ejecutivo"),
                    rx.select.content(
                        rx.foreach(
                            LeadState.ejecutivos,
                            lambda op: rx.select.item(op["nombre"], value=op["nombre"]),
                        )
                    ),
                    value=LeadState.nombre_ejecutivo,
                    on_change=LeadState.set_nombre_ejecutivo,
                    width="100%",
                ),
                direction="column",
                gap="8px",
                width="100%",
            ),
            gap="20px",
            width="100%",
        ),
        # Fila 2 — Fecha contacto / Tipo origen
        rx.flex(
            rx.flex(
                rx.text("Fecha de contacto", size="2", color_scheme="gray", weight="medium"),
                rx.input(
                    type="date",
                    value=LeadState.fecha_contacto,
                    on_change=LeadState.set_fecha_contacto,
                    width="100%",
                ),
                direction="column",
                gap="8px",
                width="100%",
            ),
            rx.flex(
                rx.text("Tipo de origen", size="2", color_scheme="gray", weight="medium"),
                rx.select.root(
                    rx.select.trigger(placeholder="Selecciona origen"),
                    rx.select.content(
                        *[rx.select.item(op, value=op) for op in tipo_origen]
                    ),
                    value=LeadState.tipo_origen,
                    on_change=LeadState.set_tipo_origen,
                    width="100%",
                ),
                direction="column",
                gap="8px",
                width="100%",
            ),
            gap="20px",
            width="100%",
        ),
        # Fila 3 — Ciudad de interés / Status
        rx.flex(
            rx.flex(
                rx.text("Ciudad de interés", size="2", color_scheme="gray", weight="medium"),
                rx.input(
                    placeholder="Ej. GUADALAJARA",
                    value=LeadState.ciudad_interes,
                    on_change=LeadState.set_ciudad_interes,
                    width="100%",
                ),
                direction="column",
                gap="8px",
                width="100%",
            ),
            rx.flex(
                rx.text("Status actual", size="2", color_scheme="gray", weight="medium"),
                rx.select.root(
                    rx.select.trigger(placeholder="Selecciona status"),
                    rx.select.content(
                        *[rx.select.item(op, value=op) for op in status_actual]
                    ),
                    value=LeadState.status_actual,
                    on_change=LeadState.set_status_actual,
                    width="100%",
                ),
                direction="column",
                gap="8px",
                width="100%",
            ),
            gap="20px",
            width="100%",
        ),
        # Fila 4 — Monto / Fecha estimada cierre
        rx.flex(
            rx.flex(
                rx.text("Monto cotización (MXN)", size="2", color_scheme="gray", weight="medium"),
                rx.input(
                    placeholder="0.00",
                    type="number",
                    value=LeadState.monto_cotizacion_mxn,
                    on_change=LeadState.set_monto,
                    width="100%",
                ),
                direction="column",
                gap="8px",
                width="100%",
            ),
            rx.flex(
                rx.text("Fecha estimada de cierre", size="2", color_scheme="gray", weight="medium"),
                rx.input(
                    type="date",
                    value=LeadState.fecha_estimada_cierre,
                    on_change=LeadState.set_fecha_cierre,
                    width="100%",
                ),
                direction="column",
                gap="8px",
                width="100%",
            ),
            gap="20px",
            width="100%",
        ),
        # Fila 5 — ID Lead / Servicio de Interés
        rx.flex(
            rx.flex(
                rx.text("ID Lead", size="2", color_scheme="gray", weight="medium"),
                rx.input(
                    placeholder="EJ. KRON-RVR-20250630-02",
                    value=LeadState.id_interno,
                    on_change=LeadState.set_id_interno,
                    width="100%",
                ),
                direction="column",
                gap="8px",
                width="100%",
            ),
            rx.flex(
                rx.text("Servicio de Interés", size="2", color_scheme="gray", weight="medium"),
                rx.input(
                    placeholder="EJ. OPERACIÓN Y MANTENIMIENTO",
                    value=LeadState.servicio_producto_interes,
                    on_change=LeadState.set_servicio_producto_interes,
                    width="100%",
                ),
                direction="column",
                gap="8px",
                width="100%",
            ),
            gap="20px",
            width="100%",
        ),
        # Línea de negocio
        rx.flex(
            rx.text("Línea de negocio", size="2", color_scheme="gray", weight="medium"),
            rx.flex(
                rx.foreach(
                    lineas_negocio,
                    lambda linea: rx.checkbox(
                        linea,
                        checked=LeadState.linea_negocio.contains(linea),
                        on_change=lambda checked, linea=linea: LeadState.toggle_linea_negocio(linea, checked),
                        size="2",
                    )
                ),
                direction="column",
                gap="8px",
                padding="8px",
                border="1px solid var(--gray-6)",
                border_radius="8px",
                max_height="200px",
                overflow_y="auto",
            ),
            direction="column",
            gap="8px",
            width="100%",
        ),
        # Seguimientos (solo en modo edición)
        rx.cond(
            LeadState.editando,
            rx.card(
                rx.vstack(
                    rx.heading("Agregar Seguimiento", size="4"),
                    formulario_seguimiento(),
                    align="start",
                    width="100%",
                    gap="12px",
                ),
                width="100%",
                margin_top="16px",
            ),
        ),
        # Error
        rx.cond(
            LeadState.error != "",
            rx.callout(
                LeadState.error,
                icon="triangle_alert",
                color_scheme="red",
                size="1",
            ),
        ),
        direction="column",
        gap="20px",
        width="100%",
        padding_y="16px",
    )

def leads_page() -> rx.Component:
    return rx.hstack(
        sidebar_top_profile(),
        rx.box(
            rx.color_mode.button(position="top-right"),
            rx.vstack(
                rx.heading("Gestión de Proyectos", size="8"),
                rx.card(
                    rx.vstack(
                        # — Fila superior: acciones —
                        rx.hstack(
                            rx.dialog.root(
                                rx.dialog.trigger(
                                    rx.button(
                                        rx.icon("plus", size=14),
                                        "Nuevo Proyecto",
                                        variant="surface",
                                        on_click=LeadState.abrir_dialog,
                                    )
                                ),
                                rx.dialog.content(
                                    rx.dialog.title(
                                        rx.cond(LeadState.editando, "Editar Proyecto", "Nuevo Proyecto")
                                    ),
                                    rx.dialog.description(
                                        rx.cond(
                                            LeadState.editando,
                                            "Modifica la información del proyecto.",
                                            "Completa la información para registrar un nuevo proyecto.",
                                        ),
                                        size="2",
                                        color_scheme="gray",
                                        margin_bottom="1em",
                                    ),
                                    rx.scroll_area(
                                        formulario_lead(),
                                        type="auto",
                                        scrollbars="vertical",
                                        style={"height": "60vh"},
                                    ),
                                    rx.hstack(
                                        rx.dialog.close(
                                            rx.button(
                                                "Cancelar",
                                                variant="soft",
                                                color_scheme="gray",
                                                on_click=LeadState.cerrar_dialog,
                                            )
                                        ),
                                        rx.button(
                                            rx.cond(
                                                LeadState.editando,
                                                "Actualizar Lead",
                                                "Guardar Lead",
                                            ),
                                            on_click=LeadState.guardar_lead,
                                            loading=LeadState.cargando,
                                        ),
                                        justify="end",
                                        width="100%",
                                        margin_top="1em",
                                    ),
                                    max_width="640px",
                                    padding="32px",
                                ),
                                open=LeadState.mostrar_dialog_editar,
                            ),
                            # Dialog eliminar
                            rx.dialog.root(
                                rx.dialog.content(
                                    rx.dialog.title("Confirmar eliminación"),
                                    rx.dialog.description(
                                        "¿Estás seguro de que deseas eliminar este lead? Esta acción no se puede deshacer.",
                                        size="2",
                                        color_scheme="gray",
                                        margin_bottom="1em",
                                    ),
                                    rx.hstack(
                                        rx.dialog.close(
                                            rx.button(
                                                "Cancelar",
                                                variant="soft",
                                                color_scheme="gray",
                                                on_click=LeadState.cerrar_dialog_eliminar,
                                            )
                                        ),
                                        rx.dialog.close(
                                            rx.button(
                                                "Sí, eliminar",
                                                variant="solid",
                                                color_scheme="red",
                                                on_click=LeadState.confirmar_eliminacion,
                                                loading=LeadState.cargando,
                                            )
                                        ),
                                        justify="end",
                                        width="100%",
                                        gap="8px",
                                    ),
                                    max_width="450px",
                                    padding="24px",
                                ),
                                open=LeadState.mostrar_dialog_eliminar,
                            ),
                            # Dialog ver lead
                            rx.dialog.root(
                                rx.dialog.content(
                                    rx.dialog.title("Detalles del Lead"),
                                    rx.scroll_area(
                                        rx.cond(
                                            LeadState.lead_actual_detalle.length() > 0,
                                            rx.flex(
                                                rx.card(
                                                    rx.vstack(
                                                        rx.heading("Información General", size="4"),
                                                        rx.grid(
                                                            rx.box(
                                                                rx.text("Cliente:", weight="bold", size="2"),
                                                                rx.hstack(
                                                                    rx.text(LeadState.lead_actual_detalle.get("nombre_cliente", ""), size="2"),
                                                                    rx.text(LeadState.lead_actual_detalle.get("apellido_cliente", ""), size="2"),
                                                                    gap="4px",
                                                                ),
                                                            ),
                                                            rx.box(
                                                                rx.text("Ejecutivo:", weight="bold", size="2"),
                                                                rx.text(LeadState.lead_actual_detalle.get("nombre_ejecutivo", ""), size="2"),
                                                            ),
                                                            rx.box(
                                                                rx.text("Status:", weight="bold", size="2"),
                                                                rx.badge(LeadState.lead_actual_detalle.get("status_actual", ""), variant="soft"),
                                                            ),
                                                            rx.box(
                                                                rx.text("Monto:", weight="bold", size="2"),
                                                                rx.text(LeadState.lead_actual_detalle.get("monto_formateado", ""), size="2"),
                                                            ),
                                                            rx.box(
                                                                rx.text("Ciudad:", weight="bold", size="2"),
                                                                rx.text(LeadState.lead_actual_detalle.get("ciudad_interes", ""), size="2"),
                                                            ),
                                                            rx.box(
                                                                rx.text("Origen:", weight="bold", size="2"),
                                                                rx.text(LeadState.lead_actual_detalle.get("tipo_origen", ""), size="2"),
                                                            ),
                                                            columns="2",
                                                            spacing="4",
                                                            width="100%",
                                                        ),
                                                        align="start",
                                                        width="100%",
                                                        gap="12px",
                                                    ),
                                                    width="100%",
                                                ),
                                                rx.card(
                                                    rx.vstack(
                                                        rx.heading("Seguimientos", size="4"),
                                                        rx.cond(
                                                            LeadState.seguimientos.length() > 0,
                                                            rx.vstack(
                                                                rx.foreach(LeadState.seguimientos, tarjeta_seguimiento),
                                                                width="100%",
                                                                gap="12px",
                                                            ),
                                                            rx.text("No hay seguimientos registrados", size="2", color_scheme="gray"),
                                                        ),
                                                        align="start",
                                                        width="100%",
                                                        gap="12px",
                                                    ),
                                                    width="100%",
                                                ),
                                                rx.card(
                                                    rx.vstack(
                                                        rx.heading("Agregar Nuevo Seguimiento", size="4"),
                                                        formulario_seguimiento(),
                                                        align="start",
                                                        width="100%",
                                                        gap="12px",
                                                    ),
                                                    width="100%",
                                                ),
                                            rx.cond(
                                                LeadState.error != "",
                                                rx.callout(
                                                    LeadState.error,
                                                    icon="triangle_alert",
                                                    color_scheme="red",
                                                    size="1",
                                                ),
                                            ),
                                            direction="column",
                                            gap="16px",
                                            width="100%",
                                        ),
                                        rx.text("Cargando información del lead...", size="2", color_scheme="gray"),
                                    ),
                                    type="auto",
                                    scrollbars="vertical",
                                    style={"height": "70vh"},
                                ),
                                    rx.flex(
                                        rx.dialog.close(
                                            rx.button(
                                                "Cerrar",
                                                variant="soft",
                                                on_click=LeadState.cerrar_dialog_ver,
                                            )
                                        ),
                                        justify="end",
                                        width="100%",
                                        margin_top="1em",
                                    ),
                                    max_width="800px",
                                    padding="32px",
                                ),
                                open=LeadState.mostrar_dialog_ver,
                            ),
                            rx.spacer(),
                            rx.heading("Lista de Proyectos", size="5"),
                            # Toggle entre vista tabla y kanban
                            rx.button(
                                rx.cond(
                                    LeadState.vista_kanban,
                                    rx.hstack(
                                        rx.icon("table", size=14),
                                        "Vista Tabla",
                                        gap="4px",
                                    ),
                                    rx.hstack(
                                        rx.icon("layout-grid", size=14),
                                        "Vista Kanban",
                                        gap="4px",
                                    ),
                                ),
                                variant="soft",
                                on_click=LeadState.toggle_vista,
                            ),
                            rx.button(
                                rx.icon("refresh-cw", size=14),
                                "Recargar",
                                variant="soft",
                                on_click=LeadState.cargar_leads,
                                loading=LeadState.cargando,
                            ),
                            align="center",
                            width="100%",
                        ),

                        # — Barra de filtros —
                        rx.hstack(
                            rx.input(
                                rx.input.slot(rx.icon("search", size=14)),
                                placeholder="Buscar por cliente, ejecutivo...",
                                value=LeadState.filtro_texto,
                                on_change=LeadState.set_filtro_texto,
                                width="300px",
                            ),
                            rx.select.root(
                                rx.select.trigger(placeholder="Filtrar por status"),
                                rx.select.content(
                                    rx.select.item("Todos los status", value="TODOS"),
                                    *[rx.select.item(op, value=op) for op in status_actual],
                                ),
                                value=LeadState.filtro_status_ui,
                                on_change=LeadState.set_filtro_status,
                            ),
                            rx.select.root(
                                rx.select.trigger(placeholder="Filtrar por origen"),
                                rx.select.content(
                                    rx.select.item("Todos los orígenes", value="TODOS"),
                                    *[rx.select.item(op, value=op) for op in tipo_origen],
                                ),
                                value=LeadState.filtro_origen_ui,
                                on_change=LeadState.set_filtro_origen,
                            ),
                            rx.select.root(
                                rx.select.trigger(placeholder="Filtrar por ejecutivo"),
                                rx.select.content(
                                    rx.select.item("Todos los ejecutivos", value="TODOS"),
                                    *[rx.select.item(op, value=op) for op in ["FERNANDO CARRANCO PALOMARES", "DIETER RASHID CONTRERAS GARCIA", "SAULO SALGADO NAVA"]],
                                ),
                                value=LeadState.filtro_ejecutivo_ui,
                                on_change=LeadState.set_filtro_ejecutivo,
                            ),
                            rx.cond(
                                (LeadState.filtro_texto != "")
                                | (LeadState.filtro_status != "")
                                | (LeadState.filtro_origen != ""),
                                rx.button(
                                    rx.icon("x", size=14),
                                    "Limpiar filtros",
                                    variant="ghost",
                                    color_scheme="gray",
                                    on_click=LeadState.limpiar_filtros,
                                ),
                            ),
                            wrap="wrap",
                            gap="8px",
                            width="100%",
                        ),

                        # — Vista condicional: Tabla o Kanban —
                        rx.cond(
                            LeadState.vista_kanban,
                            # Vista Kanban
                            kanban_view(),
                            # Vista Tabla
                            rx.box(
                                rx.table.root(
                                    rx.table.header(
                                        rx.table.row(
                                            rx.table.column_header_cell(
                                                rx.hstack(rx.icon("hash", size=12), sort_header("ID Lead", "id_interno"), align="center"),
                                                on_click=lambda: LeadState.set_sort_col("id_interno"),
                                                cursor="pointer",
                                            ),
                                            rx.table.column_header_cell(
                                                rx.hstack(rx.icon("users", size=12), sort_header("Nombre", "nombre_cliente"), align="center"),
                                                on_click=lambda: LeadState.set_sort_col("nombre_cliente"),
                                                cursor="pointer",
                                            ),
                                            rx.table.column_header_cell(
                                                rx.hstack(rx.icon("user-round", size=12), sort_header("Nombre Ejecutivo", "nombre_ejecutivo"), align="center"),
                                                on_click=lambda: LeadState.set_sort_col("nombre_ejecutivo"),
                                                cursor="pointer",
                                            ),
                                            rx.table.column_header_cell(
                                                rx.hstack(rx.icon("calendar-days", size=12), sort_header("Fecha Contacto", "fecha_contacto"), align="center"),
                                                on_click=lambda: LeadState.set_sort_col("fecha_contacto"),
                                                cursor="pointer",
                                            ),
                                            rx.table.column_header_cell(
                                                rx.hstack(rx.icon("building", size=12), sort_header("Empresa", "empresa_cliente"), align="center"),
                                                on_click=lambda: LeadState.set_sort_col("empresa_cliente"),
                                                cursor="pointer",
                                            ),
                                            rx.table.column_header_cell(
                                                rx.hstack(rx.icon("phone", size=12), sort_header("Origen", "tipo_origen"), align="center"),
                                                on_click=lambda: LeadState.set_sort_col("tipo_origen"),
                                                cursor="pointer",
                                            ),
                                            rx.table.column_header_cell(
                                                rx.hstack(rx.icon("map", size=12), sort_header("Ciudad", "ciudad_interes"), align="center"),
                                                on_click=lambda: LeadState.set_sort_col("ciudad_interes"),
                                                cursor="pointer",
                                            ),
                                            rx.table.column_header_cell(
                                                rx.hstack(rx.icon("box", size=12), sort_header("Servicio de Interés", "servicio_producto_interes"), align="center"),
                                                on_click=lambda: LeadState.set_sort_col("servicio_producto_interes"),
                                                cursor="pointer",
                                            ),
                                            rx.table.column_header_cell(
                                                rx.hstack(rx.icon("check", size=12), sort_header("Status", "status_actual"), align="center"),
                                                on_click=lambda: LeadState.set_sort_col("status_actual"),
                                                cursor="pointer",
                                            ),
                                            rx.table.column_header_cell(
                                                rx.hstack(rx.icon("dollar-sign", size=12), sort_header("Monto (MXN)", "monto_cotizacion_mxn"), align="center"),
                                                on_click=lambda: LeadState.set_sort_col("monto_cotizacion_mxn"),
                                                cursor="pointer",
                                            ),
                                            rx.table.column_header_cell(
                                                rx.hstack(rx.icon("calendar-check", size=12), sort_header("Cierre Est.", "fecha_estimada_cierre"), align="center"),
                                                on_click=lambda: LeadState.set_sort_col("fecha_estimada_cierre"),
                                                cursor="pointer",
                                            ),
                                            rx.table.column_header_cell(
                                                rx.hstack(rx.icon("briefcase-business", size=12), sort_header("Línea de Negocio", "linea_negocio"), align="center"),
                                                on_click=lambda: LeadState.set_sort_col("linea_negocio"),
                                                cursor="pointer",
                                            ),
                                            rx.table.column_header_cell("Acciones"),
                                        )
                                    ),
                                    rx.table.body(
                                        rx.foreach(LeadState.leads_paginados, fila_lead)
                                    ),
                                    variant="surface",
                                    style={
                                        "width": "max-content",
                                        "tablke_layout": "auto",
                                        "& tbody tr:nth-child(odd)": {
                                            "background": "var(--gray-1)"
                                        },
                                        "& tbody tr:nth-child(even)": {
                                            "background": "var(--gray-2)"
                                        },
                                    },
                                ),
                                overflow_x="auto",
                                width="100%",
                            ),
                        ),

                        # — Paginación (solo en vista tabla) —
                        rx.cond(
                            ~LeadState.vista_kanban,
                            paginacion(),
                        ),

                        spacing="4",
                        width="100%",
                    ),
                    width="100%",
                ),
                spacing="6",
                width="100%",
                padding="6",
            ),
            flex="1",
            overflow_y="auto",
            height="100vh",
            padding_top="1em",
            padding_left="1em",
            padding_right="1em",
        ),
        align="start",
        spacing="0",
        width="100%",
        on_mount=[LeadState.cargar_leads, init_resizable_columns()],
    )