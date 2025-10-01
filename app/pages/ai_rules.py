import reflex as rx
from app.states.ai_rules_state import (
    AIRulesState,
    AIDocType,
    AISubKategorie,
    AIKategorie,
)


def doc_type_card(doc_type: AIDocType):
    return rx.el.div(
        rx.el.h4(doc_type["name"], class_name="font-semibold text-foreground"),
        rx.el.div(
            rx.el.p(
                "Priority: ", class_name="font-medium text-sm text-muted-foreground"
            ),
            rx.el.p(doc_type["priority"], class_name="text-sm"),
            class_name="flex gap-2 items-center",
        ),
        rx.el.div(
            rx.el.p(
                "Steuer relevant: ",
                class_name="font-medium text-sm text-muted-foreground",
            ),
            rx.cond(
                doc_type["steuer_relevant"],
                rx.el.span(
                    "Yes",
                    class_name="px-2 py-1 text-xs rounded-full bg-green-100 text-green-800",
                ),
                rx.el.span(
                    "No",
                    class_name="px-2 py-1 text-xs rounded-full bg-red-100 text-red-800",
                ),
            ),
            class_name="flex gap-2 items-center",
        ),
        rx.el.p(
            "Patterns:", class_name="font-medium text-sm text-muted-foreground mt-2"
        ),
        rx.el.div(
            rx.foreach(
                doc_type["patterns"],
                lambda p: rx.el.span(
                    p,
                    class_name="bg-secondary text-secondary-foreground text-xs font-medium mr-2 mb-2 px-2.5 py-0.5 rounded-full",
                ),
            ),
            class_name="flex flex-wrap mt-1",
        ),
        class_name="bg-card p-4 rounded-lg border border-border",
    )


def sub_category_section(sub_category: AISubKategorie):
    return rx.el.div(
        rx.el.h3(
            sub_category["name"].capitalize(),
            class_name="text-lg font-semibold text-foreground mb-3",
        ),
        rx.el.div(
            rx.foreach(sub_category["doc_types"], doc_type_card),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4",
        ),
        class_name="p-4 bg-muted/50 rounded-xl mt-4",
    )


def main_category_section(category: AIKategorie):
    return rx.el.div(
        rx.el.details(
            rx.el.summary(
                rx.el.h2(
                    category["name"].capitalize(),
                    class_name="text-xl font-bold text-foreground cursor-pointer",
                )
            ),
            rx.el.div(rx.foreach(category["sub_categories"], sub_category_section)),
            class_name="p-4",
        ),
        class_name="bg-card rounded-xl border border-border mb-6",
    )


def ai_rules_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "AI Renamer Rules", class_name="text-3xl font-bold text-foreground"
            ),
            rx.el.button(
                rx.icon("save", class_name="mr-2"),
                "Save Changes",
                on_click=AIRulesState.save_rules,
                class_name="bg-primary text-primary-foreground hover:bg-primary/90 px-4 py-2 rounded-lg flex items-center font-semibold",
            ),
            class_name="flex justify-between items-center mb-6",
        ),
        rx.el.div(rx.foreach(AIRulesState.kategorien_list, main_category_section)),
        on_mount=AIRulesState.on_load,
    )