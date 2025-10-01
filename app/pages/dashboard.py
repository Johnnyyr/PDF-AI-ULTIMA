import reflex as rx
from app.state import DashboardState
from app.styles import CARD_STYLE


def api_endpoint_card() -> rx.Component:
    def endpoint_row(endpoint: dict) -> rx.Component:
        return rx.el.tr(
            rx.el.td(
                rx.el.span(
                    endpoint["method"],
                    class_name=rx.match(
                        endpoint["method"],
                        (
                            "GET",
                            "text-green-600 bg-green-50 px-2 py-0.5 font-mono text-sm",
                        ),
                        (
                            "POST",
                            "text-blue-600 bg-blue-50 px-2 py-0.5 font-mono text-sm",
                        ),
                        "text-gray-600 bg-gray-50 px-2 py-0.5 font-mono text-sm",
                    ),
                ),
                class_name="p-3",
            ),
            rx.el.td(
                rx.el.span(
                    endpoint["path"], class_name="font-mono text-sm text-gray-800"
                ),
                class_name="p-3",
            ),
            rx.el.td(
                rx.el.span(endpoint["description"], class_name="text-sm text-gray-500"),
                class_name="p-3",
            ),
        )

    return rx.el.div(
        rx.el.h2(
            "API Endpoints",
            class_name="text-xl font-bold text-black p-4 border-b border-gray-200",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Method",
                            class_name="text-left font-bold text-sm text-gray-600 p-3",
                        ),
                        rx.el.th(
                            "Path",
                            class_name="text-left font-bold text-sm text-gray-600 p-3",
                        ),
                        rx.el.th(
                            "Description",
                            class_name="text-left font-bold text-sm text-gray-600 p-3",
                        ),
                    )
                ),
                rx.el.tbody(rx.foreach(DashboardState.api_endpoints, endpoint_row)),
            ),
            class_name="w-full",
        ),
        style=CARD_STYLE,
    )


def ocr_stats_grid() -> rx.Component:
    def stat_card(stat: dict) -> rx.Component:
        return rx.el.div(
            rx.icon(stat["icon"], size=24, class_name="text-sky-500"),
            rx.el.p(stat["label"], class_name="text-sm text-muted-foreground mt-2"),
            rx.el.p(stat["value"], class_name="text-2xl font-bold text-foreground"),
            class_name="bg-card p-4 rounded-xl border border-border",
        )

    return rx.el.div(
        rx.foreach(DashboardState.ocr_stats, stat_card),
        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6",
    )


def running_processes_card() -> rx.Component:
    def process_row(process: dict) -> rx.Component:
        return rx.el.tr(
            rx.el.td(
                rx.el.span(process["pid"], class_name="text-sm text-gray-800"),
                class_name="p-3",
            ),
            rx.el.td(
                rx.el.span(process["name"], class_name="text-sm font-bold text-black"),
                class_name="p-3",
            ),
            rx.el.td(
                rx.el.div(
                    rx.el.div(
                        class_name=rx.cond(
                            process["status"] == "running",
                            "h-2 w-2 bg-green-500 rounded-full mr-2",
                            rx.cond(
                                process["status"] == "idle",
                                "h-2 w-2 bg-yellow-500 rounded-full mr-2",
                                "h-2 w-2 bg-red-500 rounded-full mr-2",
                            ),
                        )
                    ),
                    rx.el.span(str(process["status"]).capitalize()),
                    class_name="flex items-center text-sm",
                ),
                class_name="p-3",
            ),
            rx.el.td(
                rx.el.span(f"{process['cpu']}%", class_name="text-sm text-gray-600"),
                class_name="p-3 text-right",
            ),
            rx.el.td(
                rx.el.span(
                    f"{process['memory']} MB", class_name="text-sm text-gray-600"
                ),
                class_name="p-3 text-right",
            ),
        )

    return rx.el.div(
        rx.el.h2(
            "Running Processes",
            class_name="text-xl font-bold text-black p-4 border-b border-gray-200",
        ),
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th(
                        "PID",
                        class_name="text-left font-bold text-sm text-gray-600 p-3",
                    ),
                    rx.el.th(
                        "Name",
                        class_name="text-left font-bold text-sm text-gray-600 p-3",
                    ),
                    rx.el.th(
                        "Status",
                        class_name="text-left font-bold text-sm text-gray-600 p-3",
                    ),
                    rx.el.th(
                        "CPU",
                        class_name="text-right font-bold text-sm text-gray-600 p-3",
                    ),
                    rx.el.th(
                        "Memory",
                        class_name="text-right font-bold text-sm text-gray-600 p-3",
                    ),
                )
            ),
            rx.el.tbody(rx.foreach(DashboardState.running_processes, process_row)),
        ),
        style=CARD_STYLE,
    )


def dashboard_page() -> rx.Component:
    return rx.el.div(
        rx.el.h1("Dashboard", class_name="text-3xl font-bold text-black mb-6"),
        ocr_stats_grid(),
        rx.el.div(
            running_processes_card(),
            api_endpoint_card(),
            class_name="grid grid-cols-1 lg:grid-cols-1 gap-6 mt-6",
        ),
        class_name="space-y-6",
    )