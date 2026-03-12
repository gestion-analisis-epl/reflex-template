import reflex as rx
from states.lead_state import LeadState


def paginacion() -> rx.Component:
    return rx.hstack(
        rx.text(LeadState.rango_info, size="2", color_scheme="gray"),
        rx.spacer(),
        rx.hstack(
            rx.button(
                rx.icon("chevron-left", size=14),
                variant="soft",
                color_scheme="gray",
                size="2",
                disabled=LeadState.pagina_actual_int <= 1,
                on_click=LeadState.pagina_anterior,
            ),
            rx.foreach(
                LeadState.paginas_visibles,
                lambda p: rx.button(
                    p.to_string(),
                    variant=rx.cond(LeadState.pagina_actual_int == p, "solid", "soft"),
                    color_scheme=rx.cond(LeadState.pagina_actual_int == p, "blue", "gray"),
                    size="2",
                    on_click=LeadState.ir_a_pagina(p),
                    min_width="36px",
                ),
            ),
            rx.button(
                rx.icon("chevron-right", size=14),
                variant="soft",
                color_scheme="gray",
                size="2",
                disabled=LeadState.pagina_actual_int >= LeadState.total_paginas,
                on_click=LeadState.pagina_siguiente,
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
            value=LeadState.items_por_pagina_str,
            on_change=LeadState.set_items_por_pagina,
            size="2",
        ),
        align="center",
        width="100%",
        padding_top="12px",
        padding_bottom="4px",
    )