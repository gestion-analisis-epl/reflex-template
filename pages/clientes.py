import reflex as rx
from states.cliente_state import ClienteState
from utils.selectboxes import tipos_cliente, estados_mexico
from components.sidebar import sidebar_top_profile, SidebarState
from components.resizable_column import init_resizable_columns

# ── Componentes auxiliares ───────────────────────────────────────────────────

def sort_header_cliente(label: str, col: str) -> rx.Component:
    """Header de columna con indicador de ordenamiento para ClienteState"""
    return rx.hstack(
        rx.text(label, size="2", weight="medium"),
        rx.cond(
            ClienteState.sort_col == col,
            rx.cond(
                ClienteState.sort_asc,
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

def paginacion_clientes() -> rx.Component:
    """Componente de paginación para ClienteState"""
    return rx.hstack(
        rx.text(ClienteState.rango_info, size="2", color_scheme="gray"),
        rx.spacer(),
        rx.hstack(
            rx.button(
                rx.icon("chevron-left", size=14),
                variant="soft",
                color_scheme="gray",
                size="2",
                disabled=ClienteState.pagina_actual_int <= 1,
                on_click=ClienteState.pagina_anterior,
            ),
            rx.foreach(
                ClienteState.paginas_visibles,
                lambda p: rx.button(
                    p.to_string(),
                    variant=rx.cond(ClienteState.pagina_actual_int == p, "solid", "soft"),
                    color_scheme=rx.cond(ClienteState.pagina_actual_int == p, "blue", "gray"),
                    size="2",
                    on_click=ClienteState.ir_a_pagina(p),
                    min_width="36px",
                ),
            ),
            rx.button(
                rx.icon("chevron-right", size=14),
                variant="soft",
                color_scheme="gray",
                size="2",
                disabled=ClienteState.pagina_actual_int >= ClienteState.total_paginas,
                on_click=ClienteState.pagina_siguiente,
            ),
            gap="4px",
            align="center",
        ),
        rx.select.root(
            rx.select.trigger(),
            rx.select.content(
                rx.select.item("10 por página", value="10"),
                rx.select.item("20 por página", value="20"),
                rx.select.item("50 por página", value="50"),
            ),
            value=ClienteState.items_por_pagina_str,
            on_change=ClienteState.set_items_por_pagina,
            size="2",
        ),
        align="center",
        width="100%",
        padding_top="12px",
        padding_bottom="4px",
    )

# ── Dialog: Formulario Editar Cliente ────────────────────────────────────────

def dialog_editar_cliente() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Editar Cliente"),
            rx.dialog.description(
                "Modifica los datos del cliente.",
                size="2",
                color_scheme="gray",
                margin_bottom="1em",
            ),
            rx.vstack(
                rx.hstack(
                    rx.input(
                        placeholder="Nombre",
                        value=ClienteState.nombre,
                        on_change=ClienteState.set_nombre,
                        width="100%",
                    ),
                    rx.input(
                        placeholder="Apellido",
                        value=ClienteState.apellido,
                        on_change=ClienteState.set_apellido,
                        width="100%",
                    ),
                    spacing="3",
                    width="100%",
                ),
                rx.hstack(
                    rx.input(
                        placeholder="Empresa",
                        value=ClienteState.empresa,
                        on_change=ClienteState.set_empresa,
                        width="100%",
                    ),
                    rx.input(
                        placeholder="Teléfono",
                        value=ClienteState.telefono,
                        on_change=ClienteState.set_telefono,
                        width="100%",
                    ),
                    spacing="3",
                    width="100%",
                ),
                rx.input(
                    placeholder="Email",
                    value=ClienteState.email,
                    on_change=ClienteState.set_email,
                    width="100%",
                ),
                rx.select(
                    estados_mexico,
                    placeholder="Estado de Origen",
                    value=ClienteState.estado_origen,
                    on_change=ClienteState.set_estado_origen,
                    width="100%",
                ),
                rx.select(
                    tipos_cliente,
                    placeholder="Tipo de Cliente",
                    value=ClienteState.tipo,
                    on_change=ClienteState.set_tipo,
                    width="100%",
                ),
                rx.hstack(
                    rx.checkbox(
                        checked=ClienteState.activo,
                        on_change=ClienteState.set_activo,
                    ),
                    rx.text("Cliente Activo", size="2"),
                    align="center",
                ),
                rx.separator(),
                rx.cond(
                    ClienteState.error != "",
                    rx.callout(
                        ClienteState.error,
                        icon="triangle-alert",
                        color_scheme="red",
                        size="1",
                        width="100%",
                    ),
                ),
                spacing="3",
                width="100%",
            ),
            rx.hstack(
                rx.dialog.close(
                    rx.button(
                        "Cancelar",
                        variant="soft",
                        color_scheme="gray",
                    ),
                ),
                rx.button(
                    "Guardar Cambios",
                    on_click=ClienteState.actualizar_cliente,
                    loading=ClienteState.cargando,
                ),
                justify="end",
                width="100%",
                margin_top="1em",
            ),
            max_width="520px",
        ),
        open=ClienteState.mostrar_dialog_editar,
        on_open_change=ClienteState.set_mostrar_dialog_editar,
    )


# ── Dialog: Confirmar Eliminar Cliente ───────────────────────────────────────

def dialog_eliminar_cliente() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Confirmar Eliminación"),
            rx.dialog.description(
                "¿Estás seguro de que deseas eliminar este cliente? Esta acción no se puede deshacer.",
                size="2",
                color_scheme="red",
                margin_bottom="1em",
            ),
            rx.hstack(
                rx.dialog.close(
                    rx.button(
                        "No, Cancelar",
                        variant="soft",
                        color_scheme="gray",
                        on_click=ClienteState.cancelar_eliminar,
                    ),
                ),
                rx.button(
                    "Sí, Eliminar",
                    color_scheme="red",
                    on_click=ClienteState.eliminar_cliente,
                    loading=ClienteState.cargando,
                ),
                justify="end",
                width="100%",
                spacing="3",
            ),
        ),
        open=ClienteState.mostrar_dialog_eliminar,
        on_open_change=ClienteState.set_mostrar_dialog_eliminar,
    )


# ── Dialog: Formulario Nuevo Cliente ─────────────────────────────────────────

def dialog_nuevo_cliente() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("user-plus", size=16),
                "Nuevo Cliente",
                variant="solid",
            ),
        ),
        rx.dialog.content(
            rx.dialog.title("Nuevo Cliente"),
            rx.dialog.description(
                "Completa los datos para registrar un nuevo cliente.",
                size="2",
                color_scheme="gray",
                margin_bottom="1em",
            ),
            rx.vstack(
                rx.hstack(
                    rx.input(
                        placeholder="Nombre",
                        value=ClienteState.nombre,
                        on_change=ClienteState.set_nombre,
                        width="100%",
                    ),
                    rx.input(
                        placeholder="Apellido",
                        value=ClienteState.apellido,
                        on_change=ClienteState.set_apellido,
                        width="100%",
                    ),
                    spacing="3",
                    width="100%",
                ),
                rx.hstack(
                    rx.input(
                        placeholder="Empresa",
                        value=ClienteState.empresa,
                        on_change=ClienteState.set_empresa,
                        width="100%",
                    ),
                    rx.input(
                        placeholder="Teléfono",
                        value=ClienteState.telefono,
                        on_change=ClienteState.set_telefono,
                        width="100%",
                    ),
                    spacing="3",
                    width="100%",
                ),
                rx.input(
                    placeholder="Email",
                    value=ClienteState.email,
                    on_change=ClienteState.set_email,
                    width="100%",
                ),
                rx.select(
                    estados_mexico,
                    placeholder="Estado de Origen",
                    value=ClienteState.estado_origen,
                    on_change=ClienteState.set_estado_origen,
                    width="100%",
                ),
                rx.select(
                    tipos_cliente,
                    placeholder="Tipo de Cliente",
                    value=ClienteState.tipo,
                    on_change=ClienteState.set_tipo,
                    width="100%",
                ),
                rx.hstack(
                    rx.checkbox(
                        default_checked=True,
                        on_change=ClienteState.set_activo,
                    ),
                    rx.text("Cliente Activo", size="2"),
                    align="center",
                ),
                rx.cond(
                    ClienteState.error != "",
                    rx.callout(
                        ClienteState.error,
                        icon="triangle-alert",
                        color_scheme="red",
                        size="1",
                        width="100%",
                    ),
                ),
                spacing="3",
                width="100%",
            ),
            rx.hstack(
                rx.dialog.close(
                    rx.button(
                        "Cancelar",
                        variant="soft",
                        color_scheme="gray",
                    ),
                ),
                rx.button(
                    "Agregar Cliente",
                    on_click=ClienteState.crear_cliente,
                    loading=ClienteState.cargando,
                ),
                justify="end",
                width="100%",
                margin_top="1em",
            ),
            max_width="520px",
        ),
    )


# ── Tabla de clientes ─────────────────────────────────────────────────────────

def tabla_clientes() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                dialog_nuevo_cliente(),
                rx.spacer(),
                rx.heading("Lista de Clientes", size="5"),
                rx.button(
                    rx.icon("refresh-cw", size=14),
                    "Recargar",
                    variant="soft",
                    on_click=ClienteState.cargar_clientes,
                    loading=ClienteState.cargando,
                ),
                align="center",
                width="100%",
            ),
            # — Barra de filtros —
            rx.hstack(
                rx.input(
                    rx.input.slot(rx.icon("search", size=14)),
                    placeholder="Buscar por nombre, empresa, teléfono...",
                    value=ClienteState.filtro_texto,
                    on_change=ClienteState.set_filtro_texto,
                    width="300px",
                ),
                rx.select.root(
                    rx.select.trigger(placeholder="Filtrar por tipo"),
                    rx.select.content(
                        rx.select.item("Todos los tipos", value="TODOS"),
                        *[rx.select.item(op, value=op) for op in tipos_cliente],
                    ),
                    value=ClienteState.filtro_tipo_ui,
                    on_change=ClienteState.set_filtro_tipo,
                ),
                rx.select.root(
                    rx.select.trigger(placeholder="Filtrar por estado"),
                    rx.select.content(
                        rx.select.item("Todos los estados", value="TODOS"),
                        *[rx.select.item(op, value=op) for op in estados_mexico],
                    ),
                    value=ClienteState.filtro_estado_ui,
                    on_change=ClienteState.set_filtro_estado,
                ),
                rx.select.root(
                    rx.select.trigger(placeholder="Filtrar por activo"),
                    rx.select.content(
                        rx.select.item("Todos", value="TODOS"),
                        rx.select.item("Activos", value="SÍ"),
                        rx.select.item("Inactivos", value="NO"),
                    ),
                    value=ClienteState.filtro_activo_ui,
                    on_change=ClienteState.set_filtro_activo,
                ),
                rx.cond(
                    (ClienteState.filtro_texto != "")
                    | (ClienteState.filtro_tipo != "")
                    | (ClienteState.filtro_estado != "")
                    | (ClienteState.filtro_activo != ""),
                    rx.button(
                        rx.icon("x", size=14),
                        "Limpiar filtros",
                        variant="ghost",
                        color_scheme="gray",
                        on_click=ClienteState.limpiar_filtros,
                    ),
                ),
                wrap="wrap",
                gap="8px",
                width="100%",
            ),
            # — Tabla de clientes —
            rx.box(
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell(
                                sort_header_cliente("Nombre", "nombre_cliente"),
                                on_click=lambda: ClienteState.set_sort_col("nombre_cliente"),
                                cursor="pointer",
                            ),
                            rx.table.column_header_cell(
                                sort_header_cliente("Apellido", "apellido_cliente"),
                                on_click=lambda: ClienteState.set_sort_col("apellido_cliente"),
                                cursor="pointer",
                            ),
                            rx.table.column_header_cell(
                                sort_header_cliente("Empresa", "empresa_cliente"),
                                on_click=lambda: ClienteState.set_sort_col("empresa_cliente"),
                                cursor="pointer",
                            ),
                            rx.table.column_header_cell(
                                sort_header_cliente("Teléfono", "telefono_cliente"),
                                on_click=lambda: ClienteState.set_sort_col("telefono_cliente"),
                                cursor="pointer",
                            ),
                            rx.table.column_header_cell(
                                sort_header_cliente("Email", "email_cliente"),
                                on_click=lambda: ClienteState.set_sort_col("email_cliente"),
                                cursor="pointer",
                            ),
                            rx.table.column_header_cell(
                                sort_header_cliente("Estado", "estado_origen"),
                                on_click=lambda: ClienteState.set_sort_col("estado_origen"),
                                cursor="pointer",
                            ),
                            rx.table.column_header_cell(
                                sort_header_cliente("Tipo", "tipo_cliente"),
                                on_click=lambda: ClienteState.set_sort_col("tipo_cliente"),
                                cursor="pointer",
                            ),
                            rx.table.column_header_cell(
                                sort_header_cliente("Activo", "activo"),
                                on_click=lambda: ClienteState.set_sort_col("activo"),
                                cursor="pointer",
                            ),
                            rx.table.column_header_cell("Acciones"),
                        ),
                    ),
                    rx.table.body(
                        rx.foreach(
                            ClienteState.clientes_paginados,
                            lambda cliente: rx.table.row(
                                rx.table.cell(
                                    rx.cond(
                                        cliente.nombre_cliente != "SIN NOMBRE",
                                        rx.text(cliente.nombre_cliente),
                                        rx.text("")
                                    ),
                                ),
                                rx.table.cell(
                                    rx.cond(
                                        cliente.apellido_cliente != "SIN APELLIDO",
                                        rx.text(cliente.apellido_cliente),
                                        rx.text(""),
                                    ),
                                ),
                                rx.table.cell(
                                    rx.cond(
                                        cliente.empresa_cliente != "SIN INFORMACIÓN",
                                        rx.text(cliente.empresa_cliente),
                                        rx.text("")
                                    ),
                                ),
                                rx.table.cell(cliente.telefono_cliente),
                                rx.table.cell(
                                    rx.cond(
                                        cliente.email_cliente.to(str).startswith("sin_correo"),
                                        rx.text(""),
                                        rx.text(cliente.email_cliente)
                                    ),
                                ),
                                rx.table.cell(cliente.estado_origen),
                                rx.table.cell(cliente.tipo_cliente),
                                rx.table.cell(
                                    rx.cond(
                                        cliente.activo,
                                        rx.badge("SÍ", color_scheme="green", variant="solid"),
                                        rx.badge("NO", color_scheme="tomato", variant="solid"),
                                    )
                                ),
                                rx.table.cell(
                                    rx.hstack(
                                        rx.button(
                                            rx.icon("pencil", size=16),
                                            variant="soft",
                                            color_scheme="blue",
                                            on_click=ClienteState.cargar_datos_cliente(cliente.id_cliente),
                                        ),
                                        rx.button(
                                            rx.icon("trash-2", size=16),
                                            variant="soft",
                                            color_scheme="red",
                                            on_click=ClienteState.preparar_eliminar(cliente.id_cliente),
                                        ),
                                        spacing="2",
                                    )
                                ),
                            ),
                        ),
                    ),
                    variant="surface",
                    style={"min_width": "1200px", "width": "100%", "table_layout": "fixed"},
                ),
                overflow_x="auto",
                width="100%",
            ),
            # — Paginación —
            paginacion_clientes(),
            spacing="4",
            width="100%",
        ),
        width="100%",
    )

# ── Página principal ──────────────────────────────────────────────────────────

def clientes_page() -> rx.Component:
    return rx.hstack(
        sidebar_top_profile(),
        rx.box(
            rx.color_mode.button(position="top-right"),
            rx.vstack(
                rx.heading("Gestión de Clientes", size="8"),
                tabla_clientes(),
                dialog_editar_cliente(),
                dialog_eliminar_cliente(),
                spacing="6",
                width="100%",
                padding="6",
            ),
            flex="1",
            overflow_y="auto",
            height="100vh",
        ),
        align="start",
        spacing="0",
        width="100%",
        on_mount=[ClienteState.cargar_clientes, init_resizable_columns()],
    )