import reflex as rx

class SidebarState(rx.State):
    collapsed: bool = False
    
    @rx.var
    def expanded(self) -> bool:
        return not self.collapsed
    
    def toggle(self):
        self.collapsed = not self.collapsed

def sidebar_item(text: str, icon: str, href: str) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(icon),
            rx.cond(
                SidebarState.expanded,
                rx.text(text, size="3"),
            ),
            width="100%",
            padding_x="0.5rem",
            padding_y="0.75rem",
            align="center",
            justify=rx.cond(SidebarState.collapsed, "center", "start"),
            style={
                "_hover": {
                    "bg": rx.color("accent", 4),
                    "color": rx.color("accent", 11),
                },
                "border-radius": "0.5rem",
            },
        ),
        href=href,
        underline="none",
        weight="medium",
        width="100%",
    )
    
def sidebar_items() -> rx.Component:
    return rx.vstack(
        sidebar_item("Inicio", "home", "/"),
        sidebar_item("Dashboard", "layout-dashboard", "/"),
        sidebar_item("Clientes", "users", "/clientes"),
        sidebar_item("Proyectos", "file-spreadsheet", "/proyectos"),
        sidebar_item("Ventas", "banknote", "/"),
        spacing="1",
        width="100%",
    )
    
def sidebar_top_profile() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.vstack(
                rx.hstack(
                    rx.cond(
                        SidebarState.expanded,
                        rx.hstack(
                            rx.icon_button(rx.icon("user"), size="3", radius="full"),
                            rx.vstack(
                                rx.box(
                                    rx.text("Mi cuenta", size="3", weight="bold"),
                                    rx.text("@kronosambiental", size="2", weight="medium"),
                                    width="100%",
                                ),
                                spacing="0",
                                justify="start",
                                width="100%",
                            ),
                            rx.spacer(),
                            align="center",
                            width="100%",
                        ),
                    ),
                    rx.icon_button(
                        rx.cond(
                            SidebarState.expanded,
                            rx.icon("chevron-left"),
                            rx.icon("chevron-right"),
                        ),
                        on_click=SidebarState.toggle,
                        size="2",
                        variant="ghost",
                        color_scheme="gray",
                    ),
                    padding_x="0.5rem",
                    align="center",
                    justify=rx.cond(SidebarState.collapsed, "center", "between"),
                    width="100%",
                ),
                sidebar_items(),
                rx.spacer(),
                sidebar_item("Help & Support", "life-buoy", "/#"),
                spacing="5",
                padding_x="1em",
                padding_y="1.5em",
                bg=rx.color("accent", 3),
                align="start",
                height="100vh",
                width=rx.cond(SidebarState.expanded, "16em", "4em"),
                transition="width 0.3s ease",
                overflow="hidden",
            ),
        ),
        rx.mobile_and_tablet(
            rx.drawer.root(
                rx.drawer.trigger(rx.icon("align-justify", size=30)),
                rx.drawer.overlay(z_index="5"),
                rx.drawer.portal(
                    rx.drawer.content(
                        rx.vstack(
                            rx.box(
                                rx.drawer.close(rx.icon("x", size=30)),
                                width="100%",
                            ),
                            sidebar_items(),
                            rx.spacer(),
                            rx.vstack(
                                sidebar_item("Help & Support", "life-buoy", "/#"),
                                rx.divider(margin="0"),
                                rx.hstack(
                                    rx.icon_button(
                                        rx.icon("user"), size="3", radius="full"
                                    ),
                                    rx.vstack(
                                        rx.box(
                                            rx.text(
                                                "My account", size="3", weight="bold"
                                            ),
                                            rx.text(
                                                "user@reflex.dev",
                                                size="2",
                                                weight="medium",
                                            ),
                                            width="100%",
                                        ),
                                        spacing="0",
                                        justify="start",
                                        width="100%",
                                    ),
                                    padding_x="0.5rem",
                                    align="center",
                                    justify="start",
                                    width="100%",
                                ),
                                width="100%",
                                spacing="5",
                            ),
                            spacing="5",
                            width="100%",
                        ),
                        top="auto",
                        right="auto",
                        height="100%",
                        width="20em",
                        padding="1.5em",
                        bg=rx.color("accent", 2),
                    ),
                    width="100%",
                ),
                direction="left",
            ),
            padding="1em",
        ),
    )