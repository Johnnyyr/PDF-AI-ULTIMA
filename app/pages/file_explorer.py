import reflex as rx
from app.state import FileExplorerState


def file_list_item(file: dict) -> rx.Component:
    return rx.el.div(
        rx.el.button(
            rx.icon(file["icon"], class_name="w-5 h-5 mr-3"),
            rx.el.span(file["name"], class_name="truncate"),
            on_click=lambda: FileExplorerState.set_selected_file(file["name"]),
            class_name=rx.cond(
                FileExplorerState.selected_file == file["name"],
                "flex items-center w-full text-left p-2 rounded-lg bg-accent text-accent-foreground",
                "flex items-center w-full text-left p-2 rounded-lg hover:bg-accent",
            ),
        )
    )


def file_metadata() -> rx.Component:
    return rx.el.div(
        rx.el.h3("File Data", class_name="text-lg font-semibold mb-4"),
        rx.el.div(
            rx.el.p("Filename:", class_name="font-medium text-muted-foreground"),
            rx.el.p(FileExplorerState.selected_file, class_name="font-mono"),
            class_name="flex justify-between items-center text-sm mb-2",
        ),
        rx.el.div(
            rx.el.p("Size:", class_name="font-medium text-muted-foreground"),
            rx.el.p("2.1 MB", class_name="font-mono"),
            class_name="flex justify-between items-center text-sm mb-2",
        ),
        rx.el.div(
            rx.el.p("Last Modified:", class_name="font-medium text-muted-foreground"),
            rx.el.p("2024-05-23", class_name="font-mono"),
            class_name="flex justify-between items-center text-sm mb-4",
        ),
        rx.el.h3(
            "Rename",
            class_name="text-lg font-semibold mb-4 border-t border-border pt-4",
        ),
        rx.el.input(
            placeholder="New filename...",
            class_name="w-full bg-input rounded-lg p-2 text-sm mb-2",
        ),
        rx.el.button(
            "Rename File",
            class_name="w-full bg-primary text-primary-foreground p-2 rounded-lg text-sm mb-4",
        ),
        rx.el.h3(
            "Tags", class_name="text-lg font-semibold mb-4 border-t border-border pt-4"
        ),
        rx.el.div(
            rx.el.span(
                "invoice",
                class_name="bg-secondary text-secondary-foreground text-xs font-medium mr-2 px-2.5 py-0.5 rounded-full",
            ),
            rx.el.span(
                "important",
                class_name="bg-secondary text-secondary-foreground text-xs font-medium mr-2 px-2.5 py-0.5 rounded-full",
            ),
            class_name="flex flex-wrap",
        ),
        rx.el.input(
            placeholder="Add a tag...",
            class_name="w-full bg-input rounded-lg p-2 text-sm mt-2",
        ),
        class_name="bg-card p-4 rounded-xl border border-border",
    )


def pdf_preview() -> rx.Component:
    return rx.el.div(
        rx.cond(
            FileExplorerState.selected_file != "",
            rx.el.iframe(
                src=rx.get_upload_url(FileExplorerState.selected_file),
                class_name="w-full h-full rounded-xl",
            ),
            rx.el.div(
                rx.icon("file-text", size=48, class_name="text-muted-foreground"),
                rx.el.p(
                    "Select a file to preview", class_name="text-muted-foreground mt-4"
                ),
                class_name="flex flex-col items-center justify-center h-full",
            ),
        ),
        class_name="bg-card rounded-xl border border-border h-full",
    )


def file_explorer_page() -> rx.Component:
    return rx.el.div(
        rx.el.h1("File Explorer", class_name="text-3xl font-bold text-foreground mb-6"),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.input(
                            placeholder="Search files...",
                            class_name="w-full bg-input p-2 rounded-lg",
                        ),
                        class_name="p-2",
                    ),
                    rx.el.div(
                        rx.foreach(FileExplorerState.files, file_list_item),
                        class_name="space-y-1 p-2",
                    ),
                    class_name="w-1/4 bg-card rounded-xl border border-border h-[80vh] flex flex-col",
                ),
                rx.el.div(file_metadata(), class_name="w-1/4"),
                rx.el.div(pdf_preview(), class_name="w-2/4"),
                class_name="flex space-x-6 h-full",
            )
        ),
    )