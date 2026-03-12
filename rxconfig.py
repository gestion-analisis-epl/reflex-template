import reflex as rx
import os

railway_domain_env = "RAILWAY_PUBLIC_DOMAIN"

config = rx.Config(
    app_name="reflex_template",
    frontend_port=3000, # default frontend port
    backend_port=8000, # default backend port
    api_url=f'https://{os.environ[railway_domain_env]}' if railway_domain_env in os.environ else "http://127.0.0.1:8000",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)