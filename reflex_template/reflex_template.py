"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
import os
import platform
import socket
import sys
from datetime import datetime

from rxconfig import config


class State(rx.State):
    """The app state."""

    # Backend-only information (computed on the server)
    server_hostname: str = ""
    python_version: str = ""
    os_info: str = ""
    server_time: str = ""
    process_id: int = 0

    def fetch_server_info(self):
        """Fetch information that only the backend has access to."""
        self.server_hostname = socket.gethostname()
        self.python_version = sys.version.split()[0]
        self.os_info = f"{platform.system()} {platform.release()}"
        self.server_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.process_id = os.getpid()


def server_info() -> rx.Component:
    """Display backend-only server information."""
    return rx.vstack(
        rx.text("Hostname: ", State.server_hostname),
        rx.text("Python Version: ", State.python_version),
        rx.text("Operating System: ", State.os_info),
        rx.text("Server Time: ", State.server_time),
        rx.text("Process ID: ", State.process_id.to_string()),
        spacing="2",
    )


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Welcome to Reflex!", size="9"),
            rx.text(
                "Get started by editing ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
            ),
            server_info(),
            rx.link(
                rx.button("Check out our docs!"),
                href="https://reflex.dev/docs/getting-started/introduction/",
                is_external=True,
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
            on_mount=State.fetch_server_info,
        ),
    )


app = rx.App()
app.add_page(index)
