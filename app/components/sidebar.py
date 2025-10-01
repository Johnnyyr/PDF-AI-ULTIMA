import reflex as rx
from app.state import AppState


def nav_item(item: dict) -> rx.Component:
    return rx.el.button(
        rx.el.div(
            rx.icon(item["icon"], size=20, class_name="mr-3"),
            rx.el.span(item["name"]),
            class_name="flex items-center",
        ),
        on_click=lambda: AppState.set_page(item["page"]),
        class_name=rx.cond(
            AppState.current_page == item["page"],
            "w-full text-left px-4 py-2 rounded-lg text-sidebar-primary-foreground bg-sidebar-primary",
            "w-full text-left px-4 py-2 rounded-lg text-sidebar-foreground hover:bg-sidebar-accent",
        ),
    )


def sidebar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("scan-line", size=32, class_name="text-primary-foreground"),
                rx.el.h1(
                    "NUCLI",
                    class_name="text-2xl font-bold ml-2 text-primary-foreground",
                ),
                class_name="flex items-center p-4 mb-4",
            ),
            rx.el.div(
                rx.foreach(AppState.nav_items, nav_item),
                class_name="flex flex-col space-y-1 px-2",
            ),
            class_name="flex-grow",
        ),
        rx.el.div(
            rx.el.button(
                rx.cond(
                    AppState.theme == "light",
                    rx.icon("moon", class_name="mr-3"),
                    rx.icon("sun", class_name="mr-3"),
                ),
                rx.cond(AppState.theme == "light", "Dark Mode", "Light Mode"),
                on_click=AppState.toggle_theme,
                class_name="w-full flex items-center text-left px-4 py-2 rounded-lg text-sidebar-foreground hover:bg-sidebar-accent",
            ),
            rx.el.button(
                rx.icon("settings", class_name="mr-3"),
                "Settings",
                class_name="w-full flex items-center text-left px-4 py-2 rounded-lg text-sidebar-foreground hover:bg-sidebar-accent",
            ),
            rx.el.div(
                rx.image(
                    src="https://api.dicebear.com/9.x/notionists/svg?seed=user",
                    class_name="w-10 h-10 rounded-full",
                ),
                rx.el.div(
                    rx.el.p(
                        "Admin User", class_name="font-semibold text-sidebar-foreground"
                    ),
                    rx.el.p(
                        "admin@nucli.os", class_name="text-xs text-muted-foreground"
                    ),
                ),
                rx.icon("fold_vertical", class_name="text-muted-foreground"),
                class_name="flex items-center justify-between p-2 mt-4 border-t border-sidebar-border",
            ),
            class_name="p-2",
        ),
        class_name="w-64 h-screen fixed top-0 left-0 bg-sidebar border-r border-sidebar-border flex flex-col font-medium",
    )