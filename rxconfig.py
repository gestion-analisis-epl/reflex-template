import reflex as rx
import os

railway_domain_env = "RAILWAY_PUBLIC_DOMAIN"

config = rx.Config(
    app_name="kronos_crm",
    frontend_port=3000,
    backend_port=8000,
    api_url=f'https://{os.environ[railway_domain_env]}' if railway_domain_env in os.environ else "http://127.0.0.1:8000",
    state_auto_setters=True,
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)