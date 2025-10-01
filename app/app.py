import reflex as rx
from app.components.sidebar import sidebar
from app.pages.dashboard import dashboard_page
from app.pages.ocr_settings import ocr_settings_page
from app.pages.file_explorer import file_explorer_page
from app.pages.server_settings import server_settings_page
from app.pages.chat import chat_page
from app.pages.ai_rules import ai_rules_page
from app.pages.company_rules import company_rules_page
from app.state import AppState


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.match(
                AppState.current_page,
                ("Dashboard", dashboard_page()),
                ("OCR Settings", ocr_settings_page()),
                ("File Explorer", file_explorer_page()),
                ("AI Chat", chat_page()),
                ("AI Rules", ai_rules_page()),
                ("Company Rules", company_rules_page()),
                ("Server", server_settings_page()),
                rx.el.div("404 - Page not found"),
            ),
            class_name="ml-64 p-8 bg-background text-foreground transition-colors duration-300",
        ),
        class_name=rx.cond(
            AppState.theme == "dark",
            "dark font-sans bg-background min-h-screen",
            "font-sans bg-background min-h-screen",
        ),
    )


app = rx.App(
    theme=rx.theme(appearance="light", accent_color="sky"),
    stylesheets=["/styles.css"],
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, title="OCRmyPDF Dashboard")