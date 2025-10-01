import reflex as rx
from app.state import ChatState


def message_bubble(message: dict) -> rx.Component:
    is_user = message["role"] == "user"
    return rx.el.div(
        rx.el.div(
            rx.image(
                src=rx.cond(
                    is_user,
                    "https://api.dicebear.com/9.x/notionists/svg?seed=user",
                    "https://api.dicebear.com/9.x/notionists/svg?seed=assistant",
                ),
                class_name="w-8 h-8 rounded-full",
            ),
            rx.el.div(
                rx.text(message["content"], class_name="text-sm"),
                class_name="p-3 rounded-lg bg-secondary text-secondary-foreground",
            ),
            class_name=rx.cond(
                is_user, "flex items-start gap-3 justify-end", "flex items-start gap-3"
            ),
        )
    )


def chat_page() -> rx.Component:
    return rx.el.div(
        rx.el.h1("AI Chat", class_name="text-3xl font-bold text-foreground mb-6"),
        rx.el.div(
            rx.el.div(
                rx.foreach(ChatState.messages, message_bubble),
                class_name="flex-grow space-y-4 p-4 overflow-y-auto",
            ),
            rx.el.div(
                rx.el.form(
                    rx.el.input(
                        placeholder="Type your message...",
                        name="chat_input",
                        class_name="flex-grow bg-input rounded-l-lg p-2 focus:outline-none",
                    ),
                    rx.el.button(
                        rx.icon("send", class_name="w-5 h-5"),
                        type="submit",
                        class_name="bg-primary text-primary-foreground p-2 rounded-r-lg",
                    ),
                    on_submit=ChatState.send_message,
                    reset_on_submit=True,
                    class_name="flex w-full",
                ),
                class_name="p-4 border-t border-border",
            ),
            class_name="bg-card rounded-xl border border-border flex flex-col h-[80vh]",
        ),
    )