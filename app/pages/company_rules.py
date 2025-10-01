import reflex as rx
from app.states.company_rules_state import CompanyRulesState
from app.state import Company, Account


def account_item(account: Account):
    return rx.el.div(
        rx.el.p(account["name"], class_name="font-semibold"),
        rx.el.p(
            f"Alias: {account['alias']}", class_name="text-sm text-muted-foreground"
        ),
        rx.cond(
            account["iban"],
            rx.el.p(f"IBAN: {account['iban']}", class_name="text-sm font-mono"),
        ),
        rx.cond(
            account["depot_nr"],
            rx.el.p(f"Depot: {account['depot_nr']}", class_name="text-sm font-mono"),
        ),
        rx.cond(
            account["email"],
            rx.el.p(f"Email: {account['email']}", class_name="text-sm"),
        ),
        class_name="p-3 border-b border-border",
    )


def company_details() -> rx.Component:
    return rx.el.div(
        rx.cond(
            CompanyRulesState.selected_company,
            rx.el.div(
                rx.el.h3(
                    CompanyRulesState.selected_company["name"].capitalize(),
                    class_name="text-xl font-bold mb-4",
                ),
                rx.el.p("Aliases:", class_name="font-semibold mb-2"),
                rx.el.div(
                    rx.foreach(
                        CompanyRulesState.selected_company["aliases"],
                        lambda p: rx.el.span(
                            p,
                            class_name="bg-secondary text-secondary-foreground text-xs font-medium mr-2 mb-2 px-2.5 py-0.5 rounded-full",
                        ),
                    ),
                    class_name="flex flex-wrap mb-4",
                ),
                rx.el.p("Default Bucket: ", class_name="font-semibold"),
                rx.el.p(
                    CompanyRulesState.selected_company["bucket"], class_name="mb-4"
                ),
                rx.el.p("Default Category: ", class_name="font-semibold"),
                rx.el.p(
                    CompanyRulesState.selected_company["default_category"],
                    class_name="mb-4",
                ),
                rx.el.h4(
                    "Accounts",
                    class_name="text-lg font-semibold border-t border-border pt-4 mt-4 mb-2",
                ),
                rx.el.div(
                    rx.foreach(
                        CompanyRulesState.selected_company["accounts"], account_item
                    ),
                    class_name="border-t border-border rounded-lg overflow-hidden",
                ),
                class_name="p-6",
            ),
            rx.el.div(
                rx.icon("building", size=48, class_name="text-muted-foreground"),
                rx.el.p(
                    "Select a company to see details",
                    class_name="text-muted-foreground mt-4",
                ),
                class_name="flex flex-col items-center justify-center h-full",
            ),
        ),
        class_name="bg-card rounded-xl border border-border h-[80vh]",
    )


def company_list_item(company: Company) -> rx.Component:
    return rx.el.button(
        rx.el.span(company["name"].capitalize(), class_name="truncate"),
        on_click=lambda: CompanyRulesState.select_company(company["name"]),
        class_name=rx.cond(
            CompanyRulesState.selected_company["name"] == company["name"],
            "w-full text-left p-2 rounded-lg bg-accent text-accent-foreground",
            "w-full text-left p-2 rounded-lg hover:bg-accent",
        ),
        width="100%",
    )


def company_rules_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("Company Rules", class_name="text-3xl font-bold text-foreground"),
            rx.el.button(
                rx.icon("save", class_name="mr-2"),
                "Save Changes",
                on_click=CompanyRulesState.save_rules,
                class_name="bg-primary text-primary-foreground hover:bg-primary/90 px-4 py-2 rounded-lg flex items-center font-semibold",
            ),
            class_name="flex justify-between items-center mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.foreach(CompanyRulesState.companies_list, company_list_item),
                    class_name="space-y-1 p-2",
                ),
                class_name="w-1/4 bg-card rounded-xl border border-border h-[80vh] flex flex-col overflow-y-auto",
            ),
            rx.el.div(
                company_details(), class_name="w-3/4 overflow-y-auto h-[80vh] pr-2"
            ),
            class_name="flex space-x-6 h-full",
        ),
        on_mount=CompanyRulesState.on_load,
    )