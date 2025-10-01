import reflex as rx
from app.state import ServerSettingsState
from app.styles import CARD_STYLE


def log_entry_row(log: dict) -> rx.Component:
    return rx.el.div(
        rx.el.span(log["timestamp"], class_name="text-xs text-gray-400 font-mono mr-4"),
        rx.el.span(
            log["level"],
            class_name=rx.match(
                log["level"],
                ("INFO", "text-sky-600 w-12 font-bold text-xs"),
                ("DEBUG", "text-gray-500 w-12 font-bold text-xs"),
                ("ERROR", "text-red-600 w-12 font-bold text-xs"),
                "w-12 font-bold text-xs",
            ),
        ),
        rx.el.span(log["message"], class_name="text-sm font-mono text-gray-800"),
        class_name="flex items-center p-2",
    )


def server_settings_page() -> rx.Component:
    return rx.el.div(
        rx.el.h1("Server", class_name="text-3xl font-bold text-black mb-6"),
        rx.el.div(
            rx.el.h2(
                "Live Logs",
                class_name="text-xl font-bold text-black p-4 border-b border-gray-200",
            ),
            rx.el.div(
                rx.foreach(ServerSettingsState.logs, log_entry_row),
                class_name="h-[60vh] overflow-y-scroll p-2 bg-gray-50",
            ),
            style=CARD_STYLE,
        ),
    )