import reflex as rx
from states.cotizacion_state import CotizacionState
from components.sidebar import sidebar_top_profile

def formulario_cliente() -> rx.Component:
    """Formulario para datos del cliente"""
    return rx.card(
        rx.vstack(
            rx.heading("Datos del Cliente", size="4"),
            rx.flex(
                rx.text("Cliente", size="2", color_scheme="gray", weight="medium"),
                rx.select.root(
                    rx.select.trigger(placeholder="Selecciona un cliente"),
                    rx.select.content(
                        rx.foreach(
                            CotizacionState.clientes,
                            lambda cliente: rx.select.item(
                                cliente["nombre"],
                                value=cliente["nombre"],
                            ),
                        )
                    ),
                    value=CotizacionState.nombre_cliente,
                    on_change=CotizacionState.set_cliente,
                    width="100%",
                ),
                direction="column",
                gap="8px",
                width="100%",
            ),
            rx.flex(
                rx.text("Empresa", size="2", color_scheme="gray", weight="medium"),
                rx.input(
                    value=CotizacionState.empresa_cliente,
                    on_change=CotizacionState.set_empresa_cliente,
                    width="100%",
                    disabled=True,
                ),
                direction="column",
                gap="8px",
                width="100%",
            ),
            rx.flex(
                rx.text("Email", size="2", color_scheme="gray", weight="medium"),
                rx.input(
                    type="email",
                    value=CotizacionState.email_cliente,
                    on_change=CotizacionState.set_email_cliente,
                    width="100%",
                    disabled=True,
                ),
                direction="column",
                gap="8px",
                width="100%",
            ),
            rx.flex(
                rx.text("Teléfono", size="2", color_scheme="gray", weight="medium"),
                rx.input(
                    value=CotizacionState.telefono_cliente,
                    on_change=CotizacionState.set_telefono_cliente,
                    width="100%",
                    disabled=True,
                ),
                direction="column",
                gap="8px",
                width="100%",
            ),
            rx.flex(
                rx.text("Estado", size="2", color_scheme="gray", weight="medium"),
                rx.input(
                    value=CotizacionState.estado_origen,
                    on_change=CotizacionState.set_estado_origen,
                    width="100%",
                    disabled=True,
                ),
                direction="column",
                gap="8px",
                width="100%",
            ),
            align="start",
            width="100%",
            gap="16px",
        ),
        width="100%",
    )

def formulario_ejecutivo() -> rx.Component:
    """Formulario para datos del ejecutivo"""
    return rx.card(
        rx.vstack(
            rx.heading("Datos del Ejecutivo", size="4"),
            rx.flex(
                rx.text("Ejecutivo", size="2", color_scheme="gray", weight="medium"),
                rx.select.root(
                    rx.select.trigger(placeholder="Selecciona un ejecutivo"),
                    rx.select.content(
                        rx.foreach(
                            CotizacionState.ejecutivos,
                            lambda ejecutivo: rx.select.item(
                                ejecutivo["nombre"],
                                value=ejecutivo["nombre"],
                            ),
                        )
                    ),
                    value=CotizacionState.nombre_ejecutivo,
                    on_change=CotizacionState.set_ejecutivo,
                    width="100%",
                ),
                direction="column",
                gap="8px",
                width="100%",
            ),
            rx.flex(
                rx.text("Email", size="2", color_scheme="gray", weight="medium"),
                rx.input(
                    type="email",
                    value=CotizacionState.email_ejecutivo,
                    on_change=CotizacionState.set_email_ejecutivo,
                    width="100%",
                    disabled=True,
                ),
                direction="column",
                gap="8px",
                width="100%",
            ),
            rx.flex(
                rx.text("Teléfono", size="2", color_scheme="gray", weight="medium"),
                rx.input(
                    value=CotizacionState.telefono_ejecutivo,
                    on_change=CotizacionState.set_telefono_ejecutivo,
                    width="100%",
                    disabled=True,
                ),
                direction="column",
                gap="8px",
                width="100%",
            ),
            align="start",
            width="100%",
            gap="16px",
        ),
        width="100%",
    )

def formulario_fechas_impuesto() -> rx.Component:
    """Formulario para fechas e impuesto"""
    return rx.card(
        rx.vstack(
            rx.heading("Fechas e Impuesto", size="4"),
            rx.flex(
                rx.text("Fecha de cotización", size="2", color_scheme="gray", weight="medium"),
                rx.input(
                    type="date",
                    value=CotizacionState.fecha_cotizacion,
                    on_change=CotizacionState.set_fecha_cotizacion,
                    width="100%",
                ),
                direction="column",
                gap="8px",
                width="100%",
            ),
            rx.flex(
                rx.text("Fecha de vencimiento", size="2", color_scheme="gray", weight="medium"),
                rx.input(
                    type="date",
                    value=CotizacionState.fecha_vencimiento,
                    on_change=CotizacionState.set_fecha_vencimiento,
                    width="100%",
                ),
                direction="column",
                gap="8px",
                width="100%",
            ),
            rx.flex(
                rx.hstack(
                    rx.checkbox(
                        "Incluir IVA",
                        checked=CotizacionState.incluir_iva,
                        on_change=CotizacionState.set_incluir_iva,
                    ),
                    align="center",
                    width="100%",
                ),
                direction="column",
                gap="8px",
                width="100%",
            ),
            rx.cond(
                CotizacionState.incluir_iva,
                rx.flex(
                    rx.text("Porcentaje de IVA (%)", size="2", color_scheme="gray", weight="medium"),
                    rx.hstack(
                        rx.input(
                            type="number",
                            step="1",
                            min="0",
                            max="100",
                            placeholder="16",
                            value=CotizacionState.impuesto_porcentaje,
                            on_change=CotizacionState.set_impuesto_porcentaje,
                            width="100%",
                        ),
                        rx.text("%", size="3", color_scheme="gray", weight="medium"),
                        align="center",
                        gap="8px",
                        width="100%",
                    ),
                    direction="column",
                    gap="8px",
                    width="100%",
                ),
            ),
            align="start",
            width="100%",
            gap="16px",
        ),
        width="100%",
    )

def dialog_agregar_producto() -> rx.Component:
    """Dialog para agregar un producto"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Agregar Producto"),
            rx.vstack(
                rx.flex(
                    rx.text("Nombre del producto", size="2", color_scheme="gray", weight="medium"),
                    rx.input(
                        placeholder="Nombre del producto",
                        value=CotizacionState.nombre_producto,
                        on_change=CotizacionState.set_nombre_producto,
                        width="100%",
                    ),
                    direction="column",
                    gap="8px",
                    width="100%",
                ),
                rx.flex(
                    rx.text("Precio unitario", size="2", color_scheme="gray", weight="medium"),
                    rx.input(
                        type="number",
                        step="0.01",
                        placeholder="0.00",
                        value=CotizacionState.precio_unitario,
                        on_change=CotizacionState.set_precio_unitario,
                        width="100%",
                    ),
                    direction="column",
                    gap="8px",
                    width="100%",
                ),
                rx.flex(
                    rx.text("Cantidad", size="2", color_scheme="gray", weight="medium"),
                    rx.input(
                        type="number",
                        placeholder="1",
                        value=CotizacionState.cantidad,
                        on_change=CotizacionState.set_cantidad,
                        width="100%",
                    ),
                    direction="column",
                    gap="8px",
                    width="100%",
                ),
                rx.cond(
                    CotizacionState.error != "",
                    rx.callout(
                        CotizacionState.error,
                        icon="triangle_alert",
                        color_scheme="red",
                        size="1",
                    ),
                ),
                rx.hstack(
                    rx.dialog.close(
                        rx.button(
                            "Cancelar",
                            variant="soft",
                            color_scheme="gray",
                            on_click=CotizacionState.cerrar_dialog_producto,
                        )
                    ),
                    rx.button(
                        "Agregar",
                        on_click=CotizacionState.agregar_producto,
                    ),
                    justify="end",
                    width="100%",
                    margin_top="1em",
                ),
                align="start",
                width="100%",
                gap="16px",
            ),
            max_width="450px",
            padding="24px",
        ),
        open=CotizacionState.mostrar_dialog_producto,
    )

def tabla_productos() -> rx.Component:
    """Tabla de productos agregados"""
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.heading("Productos", size="4"),
                rx.spacer(),
                rx.button(
                    rx.icon("plus", size=14),
                    "Agregar Producto",
                    variant="soft",
                    on_click=CotizacionState.abrir_dialog_producto,
                ),
                width="100%",
            ),
            rx.cond(
                CotizacionState.productos.length() > 0,
                rx.vstack(
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("Producto"),
                                rx.table.column_header_cell("Precio Unit."),
                                rx.table.column_header_cell("Cantidad"),
                                rx.table.column_header_cell("Total"),
                                rx.table.column_header_cell("Acciones"),
                            ),
                        ),
                        rx.table.body(
                            rx.foreach(
                                CotizacionState.productos,
                                lambda producto, index: rx.table.row(
                                    rx.table.cell(producto["nombre_producto"]),
                                    rx.table.cell(producto["precio_unitario"]),
                                    rx.table.cell(producto["cantidad"]),
                                    rx.table.cell(producto["total"]),
                                    rx.table.cell(
                                        rx.button(
                                            rx.icon("trash-2", size=14),
                                            variant="soft",
                                            color_scheme="red",
                                            size="1",
                                            on_click=lambda: CotizacionState.eliminar_producto(index),
                                        )
                                    ),
                                ),
                            )
                        ),
                        width="100%",
                    ),
                    rx.vstack(
                        rx.divider(),
                        rx.text("Los totales se calcularán al guardar la cotización", size="2", color_scheme="gray", align="right"),
                        align="end",
                        width="100%",
                        padding_top="8px",
                    ),
                    width="100%",
                    gap="12px",
                ),
                rx.text("No hay productos agregados", size="2", color_scheme="gray"),
            ),
            align="start",
            width="100%",
            gap="16px",
        ),
        width="100%",
    )

def formulario_cotizacion() -> rx.Component:
    """Formulario completo de cotización"""
    return rx.vstack(
        rx.heading(f"Cotización: {CotizacionState.id_kronos}", size="5"),
        formulario_cliente(),
        formulario_ejecutivo(),
        formulario_fechas_impuesto(),
        tabla_productos(),
        dialog_agregar_producto(),
        align="start",
        width="100%",
        gap="16px",
    )

def fila_cotizacion(cotizacion: dict) -> rx.Component:
    """Fila de la tabla de cotizaciones"""
    return rx.table.row(
        rx.table.cell(cotizacion["id_kronos"]),
        rx.table.cell(cotizacion["nombre_cliente"]),
        rx.table.cell(cotizacion["empresa_cliente"]),
        rx.table.cell(cotizacion["nombre_ejecutivo"]),
        rx.table.cell(
            rx.cond(
                cotizacion["fecha_cotizacion"],
                cotizacion["fecha_cotizacion"].to(str).split("T")[0],
                "—",
            )
        ),
        rx.table.cell(
            rx.hstack(
                rx.button(
                    rx.icon("file-text", size=16),
                    variant="soft",
                    color_scheme="blue",
                    size="1",
                    on_click=lambda: CotizacionState.generar_pdf(cotizacion["id_kronos"]),
                ),
                gap="8px",
            )
        ),
    )
    
def cotizaciones_page() -> rx.Component:
    return rx.hstack(
        sidebar_top_profile(),
        rx.box(
            rx.color_mode.button(position="top-right"),
            rx.vstack(
                rx.heading("Gestión de Cotizaciones", size="8"),
                rx.card(
                    rx.vstack(
                        rx.hstack(
                            rx.dialog.root(
                                rx.dialog.trigger(
                                    rx.button(
                                        rx.icon("plus", size=14),
                                        "Nueva Cotización",
                                        variant="surface",
                                        on_click=CotizacionState.abrir_dialog_nueva,
                                    )
                                ),
                                rx.dialog.content(
                                    rx.dialog.title("Nueva Cotización"),
                                    rx.scroll_area(
                                        formulario_cotizacion(),
                                        type="auto",
                                        scrollbars="vertical",
                                        style={"height": "70vh"},
                                    ),
                                    rx.flex(
                                        rx.dialog.close(
                                            rx.button(
                                                "Cancelar",
                                                variant="soft",
                                                color_scheme="gray",
                                                on_click=CotizacionState.cerrar_dialog_nueva,
                                            )
                                        ),
                                        rx.button(
                                            "Guardar y Generar PDF",
                                            on_click=CotizacionState.guardar_cotizacion,
                                            loading=CotizacionState.cargando,
                                        ),
                                        justify="end",
                                        width="100%",
                                        gap="8px",
                                        margin_top="1em",
                                    ),
                                    max_width="900px",
                                    padding="32px",
                                ),
                                open=CotizacionState.mostrar_dialog_nueva,
                            ),
                            rx.spacer(),
                            rx.heading("Lista de Cotizaciones", size="5"),
                            rx.button(
                                rx.icon("refresh-cw", size=14),
                                "Recargar",
                                variant="soft",
                                on_click=CotizacionState.cargar_cotizaciones,
                                loading=CotizacionState.cargando,
                            ),
                            width="100%",
                            align="center",
                        ),
                        rx.cond(
                            CotizacionState.error != "",
                            rx.callout(
                                CotizacionState.error,
                                icon="triangle_alert",
                                color_scheme="red",
                                size="1",
                            ),
                        ),
                        rx.table.root(
                            rx.table.header(
                                rx.table.row(
                                    rx.table.column_header_cell("ID"),
                                    rx.table.column_header_cell("Cliente"),
                                    rx.table.column_header_cell("Empresa"),
                                    rx.table.column_header_cell("Ejecutivo"),
                                    rx.table.column_header_cell("Fecha"),
                                    rx.table.column_header_cell("Acciones"),
                                ),
                            ),
                            rx.table.body(
                                rx.foreach(CotizacionState.cotizaciones, fila_cotizacion)
                            ),
                            width="100%",
                        ),
                        gap="16px",
                        width="100%",
                    ),
                    width="100%",
                ),
                gap="24px",
                padding="24px",
                width="100%",
            ),
            width="100%",
            padding="16px",
        ),
        width="100%",
        spacing="0",
    )
