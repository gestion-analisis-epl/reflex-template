from components.sidebar import sidebar_top_profile
import reflex as rx
from typing import Any
from reflex.components.component import field
from reflex.components.recharts.general import GraphingTooltip as BaseGraphingTooltip
from reflex.components.recharts.cartesian import XAxis as BaseXAxis, YAxis as BaseYAxis
from reflex.vars.base import Var
from states.dashboard_state import DashboardState  
from components.sidebar import sidebar_top_profile


class GraphingTooltip(BaseGraphingTooltip):
    """Extiende GraphingTooltip para habilitar formatter en Recharts."""

    formatter: Var[Any] = field(
        default=Var(_js_expr="undefined"),
        is_javascript_property=True,
    )


class XAxis(BaseXAxis):
    """Extiende XAxis para habilitar tickFormatter en Recharts."""

    tick_formatter: Var[Any] = field(
        default=Var(_js_expr="undefined"),
        is_javascript_property=True,
    )


class YAxis(BaseYAxis):
    """Extiende YAxis para habilitar tickFormatter en Recharts."""

    tick_formatter: Var[Any] = field(
        default=Var(_js_expr="undefined"),
        is_javascript_property=True,
    )


def eje_mxn_formatter() -> Var[Any]:
    return Var(
        _js_expr="(value) => `$${Number(value ?? 0).toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`"
    )


def tooltip_moneda() -> rx.Component:
    """Tooltip para montos con prefijo y unidad de moneda."""
    return GraphingTooltip.create(
        separator=": ",
        formatter=Var(
            _js_expr="(value) => `$${Number(value ?? 0).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`"
        ),
    )

def metric_card(titulo: str, valor: rx.Var | str, icono: str, color: str = "blue", sufijo: str = "") -> rx.Component:
    """Componente reutilizable para tarjetas de métricas"""
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.icon(icono, size=20, color=color),
                rx.text(titulo, size="2", color="gray", weight="medium"),
                justify="between",
                width="100%",
            ),
            rx.hstack(
                rx.heading(valor, size="7", color=color),
                rx.text(sufijo, size="3", color="gray") if sufijo else rx.box(),
                align="end",
                spacing="1",
            ),
            spacing="2",
            align="start",
        ),
        width="100%",
    )


def filtros_section() -> rx.Component:
    """Sección de filtros avanzados"""
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.heading("Filtros", size="5"),
                rx.badge(rx.text(DashboardState.total_leads, " de ", DashboardState.total_leads_sin_filtro), variant="soft", color="blue"),
                justify="between",
                width="100%",
            ),
            
            rx.grid(
                # Estado de origen
                rx.vstack(
                    rx.text("Estado origen:", weight="bold", size="2"),
                    rx.select(
                        DashboardState.estados_origen_unicos,
                        value=DashboardState.filtro_estado_origen,
                        on_change=DashboardState.cambiar_filtro_estado_origen,
                        width="100%",
                    ),
                    spacing="1",
                    width="100%",
                ),
                
                # Tipo de cliente
                rx.vstack(
                    rx.text("Tipo cliente:", weight="bold", size="2"),
                    rx.select(
                        DashboardState.tipos_cliente_unicos,
                        value=DashboardState.filtro_tipo_cliente,
                        on_change=DashboardState.cambiar_filtro_tipo_cliente,
                        width="100%",
                    ),
                    spacing="1",
                    width="100%",
                ),
                
                # Línea de negocio
                rx.vstack(
                    rx.text("Línea negocio:", weight="bold", size="2"),
                    rx.select(
                        DashboardState.lineas_negocio_unicas,
                        value=DashboardState.filtro_linea_negocio,
                        on_change=DashboardState.cambiar_filtro_linea_negocio,
                        width="100%",
                    ),
                    spacing="1",
                    width="100%",
                ),
                
                # Ciudad
                rx.vstack(
                    rx.text("Ciudad:", weight="bold", size="2"),
                    rx.select(
                        DashboardState.ciudades_unicas,
                        value=DashboardState.filtro_ciudad,
                        on_change=DashboardState.cambiar_filtro_ciudad,
                        width="100%",
                    ),
                    spacing="1",
                    width="100%",
                ),

                rx.vstack(
                    rx.text("Status:", weight="bold", size="2"),
                    rx.select(
                        DashboardState.status_unicos,
                        value=DashboardState.filtro_status,
                        on_change=DashboardState.cambiar_filtro_status,
                        width="100%"
                    ),
                    spacing="1",
                    width="100%"
                ),
                
                columns="5",
                spacing="3",
                width="100%",
            ),
            
            # Búsqueda
            rx.vstack(
                rx.text("Buscar:", weight="bold", size="2"),
                rx.input(
                    placeholder="Buscar por nombre, apellido o empresa...",
                    value=DashboardState.filtro_busqueda,
                    on_change=DashboardState.cambiar_busqueda,
                    width="100%",
                ),
                spacing="1",
                width="100%",
            ),
            
            # Botones de acción
            rx.hstack(
                rx.button(
                    rx.icon("filter-x", size=16),
                    "Limpiar filtros",
                    on_click=DashboardState.limpiar_filtros,
                    variant="soft",
                    size="2",
                ),
                rx.button(
                    rx.icon("refresh-cw", size=16),
                    "Recargar datos",
                    on_click=DashboardState.cargar_leads,
                    loading=DashboardState.is_loading,
                    size="2",
                ),
                spacing="2",
            ),
            
            spacing="4",
            width="100%",
        ),
        width="100%",
    )


def metricas_principales() -> rx.Component:
    """Métricas clave del dashboard"""
    return rx.grid(
        metric_card(
            "Total Proyectos",
            DashboardState.total_leads,
            "users",
            "blue"
        ),
        metric_card(
            "Cotización Total",
            rx.text("$", DashboardState.monto_total_cotizaciones_formateado),
            "dollar-sign",
            "green",
            "MXN"
        ),
        metric_card(
            "Cotización Promedio",
            rx.text("$", DashboardState.monto_promedio_cotizacion_formateado),
            "trending-up",
            "purple",
            "MXN"
        ),
        metric_card(
            "Estados Únicos",
            DashboardState.leads_por_estado_origen.length(),
            "pie-chart",
            "orange"
        ),
        columns="4",
        spacing="4",
        width="100%",
    )


def grafico_estado_origen() -> rx.Component:
    """Gráfico de distribución por estado de origen"""
    return rx.card(
        rx.vstack(
            rx.heading("Total por Estado", size="5"),
            rx.recharts.bar_chart(
                rx.recharts.bar(
                    rx.recharts.label_list(
                        data_key="total_fmt",
                        position="right",
                    ),
                    data_key="total",
                    unit=" MXN",
                    name="Monto",
                    fill="#3b82f6",
                    radius=8,
                ),
                XAxis.create(
                    type_="number",
                    tick_formatter=eje_mxn_formatter(),
                ),
                rx.recharts.y_axis(
                    data_key="estado",
                    type_="category",
                    width=120,
                ),
                tooltip_moneda(),
                data=DashboardState.total_por_estado_origen,
                layout="vertical",
                height=300,
                width="100%",
                margin={"top": 20, "right": 80, "bottom": 20, "left": 20},
            ),
            spacing="3",
            width="100%",
        ),
        width="100%",
    )

def grafico_linea_negocio() -> rx.Component:
    """Gráfico de líneas de negocio"""
    COLORS = ["#ab62c0", "#6366f1", "#22d3ee", "#f59e0b", "#10b981", "#ef4444", "#3b82f6", "#ec4899", "#84cc16", "#64748b"]

    return rx.card(
        rx.vstack(
            rx.heading("Leads por Línea de Negocio", size="5"),
            rx.recharts.pie_chart(
                rx.recharts.pie(
                    *[
                        rx.recharts.cell(fill=COLORS[i % len(COLORS)])
                        for i in range(len(COLORS))
                    ],
                    data=DashboardState.leads_por_linea_negocio,
                    data_key="cantidad",
                    name_key="linea",
                    label=True,
                    stroke="#ffffff",      # línea blanca entre sectores
                    stroke_width=2,        # grosor del borde
                ),
                rx.recharts.legend(),
                rx.recharts.tooltip(),
                height=300,
                width="100%",
            ),
            spacing="3",
            width="100%",
        ),
        width="100%",
    )

def grafico_ejecutivos() -> rx.Component:
    """Top ejecutivos por monto de cotizaciones"""
    return rx.card(
        rx.vstack(
            rx.heading("Cotizaciones por Ejecutivo", size="5"),
            rx.recharts.bar_chart(
                rx.recharts.bar(
                    rx.recharts.label_list(
                        data_key="monto_fmt",
                        position="top",
                    ),
                    data_key="monto",
                    unit=" MXN",
                    name="Monto",
                    fill="#10b981",
                ),
                rx.recharts.x_axis(data_key="ejecutivo"),
                YAxis.create(
                    width=80,
                    tick_formatter=eje_mxn_formatter(),
                ),
                tooltip_moneda(),
                data=DashboardState.cotizaciones_por_ejecutivo,
                height=300,
                width="100%",
                margin={"top": 40, "right": 20, "bottom": 20, "left": 20},
            ),
            spacing="3",
            width="100%",
        ),
        width="100%",
    )

def grafico_funnel_ventas() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading("Funnel de Ventas", size="5"),
            rx.recharts.funnel_chart(
                rx.recharts.funnel(
                    rx.recharts.label_list(
                        position="inside",
                        data_key="status",
                        fill="#FFFFFF",
                        stroke="none",
                    ),
                    data_key="cantidad",
                    name_key="status",
                    data=DashboardState.leads_por_status,
                    is_animation_active=True,
                    margin={"top": 20, "right": 20, "bottom": 20, "left": 20},
                ),
                rx.recharts.graphing_tooltip(),
                rx.recharts.legend(),
                width="100%",
                height=300,
            ),
        ),
        width="100%",
    )

def grafico_ciudades() -> rx.Component:
    """Top 10 ciudades"""
    return rx.card(
        rx.vstack(
            rx.heading("Top 10 Ciudades", size="5"),
            rx.recharts.bar_chart(
                rx.recharts.bar(
                    data_key="cantidad",
                    fill="#f59e0b",
                ),
                rx.recharts.x_axis(data_key="ciudad", angle=-45, text_anchor="end", height=100),
                rx.recharts.y_axis(),
                rx.recharts.tooltip(),
                data=DashboardState.leads_por_ciudad,
                height=350,
                width="100%",
            ),
            spacing="3",
            width="100%",
        ),
        width="100%",
    )


def grafico_tipo_cliente() -> rx.Component:
    """Gráfico de distribución por estado de origen"""
    return rx.card(
        rx.vstack(
            rx.heading("Total por Tipo de Cliente", size="5"),
            rx.recharts.bar_chart(
                rx.recharts.bar(
                    rx.recharts.label_list(
                        data_key="total_fmt",
                        position="right",
                    ),
                    data_key="total",
                    unit=" MXN",
                    name="Monto",
                    fill="#016144",
                    radius=8,
                ),
                XAxis.create(
                    type_="number",
                    tick_formatter=eje_mxn_formatter(),
                ),
                rx.recharts.y_axis(
                    data_key="tipo",
                    type_="category",
                    width=120,
                ),
                tooltip_moneda(),
                data=DashboardState.monto_cotizacion_por_tipo,
                layout="vertical",
                height=300,
                width="100%",
                margin={"top": 20, "right": 80, "bottom": 20, "left": 20},
            ),
            spacing="3",
            width="100%",
        ),
        width="100%",
    )

def tabla_leads() -> rx.Component:
    """Tabla detallada de leads"""
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.heading("Detalle de Leads", size="5"),
                rx.badge(rx.text(DashboardState.total_leads, " registros"), variant="soft"),
                justify="between",
                width="100%",
            ),
            
            rx.cond(
                DashboardState.is_loading,
                rx.center(
                    rx.spinner(size="3"),
                    padding="8",
                ),
                rx.cond(
                    DashboardState.total_leads > 0,

                    rx.data_table(
                        data=DashboardState.leads_filtrados,
                        columns=[
                            "nombre_cliente",
                            "apellido_cliente",
                            "empresa_cliente",
                            "estado_origen",
                            "tipo_cliente",
                            "nombre_ejecutivo",
                            "linea_negocio",
                            "ciudad_interes",
                            "monto_cotizacion_mxn",
                            "fecha_contacto",
                        ],
                        pagination=True,
                        search=False,
                        sort=True,
                        resizable=True,
                    ),
                    rx.callout(
                        "No hay leads que coincidan con los filtros seleccionados",
                        icon="info",
                        color="blue",
                    ),
                ),
            ),
            
            spacing="3",
            width="100%",
        ),
        width="100%",
    )


def dashboard_page() -> rx.Component:
    return rx.hstack(
        sidebar_top_profile(),
        rx.box(
            rx.color_mode.button(position="top-right"),
            rx.vstack(
                # Header
                rx.hstack(
                    rx.heading("Dashboard de Leads", size="8"),
                    rx.badge("En vivo", color_scheme="green", variant="soft"),
                    justify="between",
                    align="center",
                    width="100%",
                    padding_top="1em",
                    padding_right="1em",
                    padding_left="1em",
                ),
                
                # Mensaje de error
                rx.cond(
                    DashboardState.error_message != "",
                    rx.callout(
                        DashboardState.error_message,
                        icon="circle-alert",
                        color="red",
                    ),
                ),
                
                # Filtros
                filtros_section(),
                
                # Métricas principales
                metricas_principales(),
                
                # Gráficos - Primera fila
                rx.grid(
                    grafico_estado_origen(),
                    grafico_linea_negocio(),
                    columns="2",
                    spacing="4",
                    width="100%",
                ),
                
                # Gráficos - Segunda fila
                rx.grid(
                    grafico_ejecutivos(),
                    grafico_funnel_ventas(),
                    columns="2",
                    spacing="4",
                    width="100%",
                ),
                
                # Tabla de datos
                grafico_tipo_cliente(),
                
                spacing="5",
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
        on_mount=DashboardState.cargar_leads,
    )