# reflex_app.py
import reflex as rx
from rxconfig import config
from pages.clientes import clientes_page
from pages.leads import leads_page
from pages.cotizaciones import cotizaciones_page
from pages.dashboard import dashboard_page
from components.sidebar import sidebar_top_profile
from states.cliente_state import ClienteState
from states.lead_state import LeadState
from states.cotizacion_state import CotizacionState
from states.dashboard_state import DashboardState
from utils.scrape_news import scrape_water_news

style = {
    "font-family": "'Poppins', sans-serif",
    "font-size": "16px",
}

def index() -> rx.Component:
    noticias = scrape_water_news()

    return rx.flex(
        sidebar_top_profile(),
        rx.box(
            rx.vstack(
                rx.box(
                    rx.image(
                        src="https://images.unsplash.com/photo-1559825481-12a05cc00344?q=80&w=1065&auto=format&fit=crop",
                        width="100%", height="100%", object_fit="cover",
                        filter="blur(4px)", transform="scale(1.05)",
                        position="absolute", top="0", left="0",
                    ),
                    rx.box(
                        background="linear-gradient(to top, rgba(0,0,0,0.7), rgba(0,0,0,0.2))",
                        position="absolute", top="0", left="0", right="0", bottom="0",
                    ),
                    rx.box(
                        rx.heading("Kronos Ambiental", size="9", color="white"),
                        rx.text.em("Pasión por el agua", size="5", color="white"),
                        rx.text("Generamos soluciones ecológica, somos especialistas en el reúso y tratamiento de aguas residuales.", size="3", color="white"),
                        position="absolute", bottom="1em", left="1.5em",
                    ),
                    position="relative", width="100%", height="200px", margin_top="1em", margin_bottom="0.5em",
                    border_radius="12px", overflow="hidden",
                ),
                rx.text("Accesos Rapidos", size="4", color_scheme="gray"),
                rx.grid(
                    rx.card(
                        rx.vstack(
                            rx.card(rx.icon("layout-dashboard"), width="50px", bg="#3d85c6", display="flex"),
                            rx.vstack(rx.text("Dashboard de Métricas", weight="bold", size="4"), rx.text("Visualiza indicadores clave en tiempo real y monitorea el desempeño general del negocio", size="2", color_scheme="gray"), spacing="1"),
                            rx.link("Ver Dashboard", href="/dashboard"),
                            spacing="2", align="start", height="100%", justify="between",
                        ), padding="4",
                    ),
                    rx.card(
                        rx.vstack(
                            rx.card(rx.icon("users"), width="50px", bg="#458B74", display="flex"),
                            rx.vstack(rx.text("Clientes", weight="bold", size="4"), rx.text("Administra y consulta la información de tus clientes.", size="2", color_scheme="gray"), spacing="1"),
                            rx.link("Ver Clientes", href="/clientes"),
                            spacing="2", align="start", height="100%", justify="between",
                        ), padding="4",
                    ),
                    rx.card(
                        rx.vstack(
                            rx.card(rx.icon("banknote"), width="50px", bg="#e69138", display="flex"),
                            rx.vstack(rx.text("Proyectos", weight="bold", size="4"), rx.text("Administra y consulta la información de tus proyectos.", size="2", color_scheme="gray"), spacing="1"),
                            rx.link("Ver Proyectos", href="/proyectos"),
                            spacing="2", align="start", height="100%", justify="between",
                        ), padding="4",
                    ),
                    columns="3", spacing="4", width="100%",
                ),
                rx.vstack(
                    rx.heading("Noticias de la Industria Hidráulica", size="5", color_scheme="teal"),
                    rx.grid(
                        *[
                            rx.card(
                                rx.vstack(
                                    rx.image(src=n["img"], width="100%", height="120px", object_fit="cover", border_radius="6px"),
                                    rx.vstack(
                                        rx.text(n["title"], weight="bold", size="2"),
                                        rx.text(n["summary"], size="1", color_scheme="gray"),
                                        spacing="1",
                                    ),
                                    rx.link(rx.button("Leer más", size="1", variant="soft"), href=n["link"]),
                                    spacing="2", align="start",
                                ), padding="3",
                            )
                            for n in noticias
                        ],
                        columns="4", spacing="4", width="100%",
                    ),
                    spacing="3", width="100%", align="start",
                ),
                spacing="5", width="100%", align="start",
            ),
            flex="1", padding="6", padding_left="4em", padding_right="4em",
        ),
        direction="row", align_items="stretch", width="100vw", height="100vh",
    )

app = rx.App(style=style)
app.add_page(index)
app.add_page(clientes_page, route="/clientes", on_load=ClienteState.cargar_clientes)
app.add_page(leads_page, route="/proyectos", on_load=LeadState.cargar_leads)
app.add_page(cotizaciones_page, route="/cotizaciones", on_load=CotizacionState.cargar_cotizaciones)
app.add_page(dashboard_page, route="/dashboard")