import reflex as rx
from app.state import OCRSettingsState
from app.styles import CARD_STYLE, BUTTON_STYLE


def flat_toggle(is_on: rx.Var[bool], on_change: rx.event.EventHandler) -> rx.Component:
    return rx.el.button(
        rx.el.div(
            class_name=rx.cond(
                is_on,
                "h-4 w-4 bg-white transform translate-x-5",
                "h-4 w-4 bg-white transform translate-x-1",
            )
        ),
        on_click=on_change,
        class_name=rx.cond(
            is_on,
            "w-10 h-6 flex items-center bg-sky-500",
            "w-10 h-6 flex items-center bg-gray-300",
        ),
    )


def setting_row(setting: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.label(setting["label"], class_name="font-bold text-base text-black"),
            rx.el.p(setting["description"], class_name="text-sm text-gray-500"),
            class_name="flex-1",
        ),
        rx.el.div(
            rx.match(
                setting["type"],
                (
                    "toggle",
                    flat_toggle(
                        setting["value"],
                        lambda: OCRSettingsState.toggle_setting(setting["key"]),
                    ),
                ),
                (
                    "text",
                    rx.el.input(
                        default_value=setting["value"],
                        on_change=lambda val: OCRSettingsState.set_text_setting(
                            setting["key"], val
                        ),
                        class_name="h-[40px] w-48 border border-gray-300 px-2 focus:border-sky-500 focus:outline-none",
                    ),
                ),
                (
                    "select",
                    rx.el.select(
                        rx.foreach(
                            setting["options"], lambda opt: rx.el.option(opt, value=opt)
                        ),
                        default_value=setting["value"].to(str),
                        on_change=lambda val: OCRSettingsState.set_text_setting(
                            setting["key"], val
                        ),
                        class_name="h-[40px] w-48 border border-gray-300 px-2 focus:border-sky-500 focus:outline-none bg-white",
                    ),
                ),
            ),
            class_name="w-48 flex justify-end items-center",
        ),
        class_name="flex justify-between items-center p-4",
    )


def ocr_settings_page() -> rx.Component:
    return rx.el.div(
        rx.el.h1("OCR Settings", class_name="text-3xl font-bold text-black mb-6"),
        rx.el.div(
            rx.el.h2(
                "OCRmyPDF Parameters",
                class_name="text-xl font-bold text-black p-4 border-b border-gray-200",
            ),
            rx.el.div(
                rx.foreach(OCRSettingsState.settings, setting_row),
                class_name="divide-y divide-gray-200",
            ),
            rx.el.div(
                rx.el.button(
                    "Save Changes",
                    on_click=OCRSettingsState.save_settings,
                    style=BUTTON_STYLE,
                    class_name="px-6",
                ),
                class_name="p-4 border-t border-gray-200 flex justify-end",
            ),
            style=CARD_STYLE,
        ),
    )