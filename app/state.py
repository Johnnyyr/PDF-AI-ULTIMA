import reflex as rx
from typing import TypedDict, Literal, Optional
import yaml


class NavItem(TypedDict):
    name: str
    icon: str
    page: str


class ApiEndpoint(TypedDict):
    method: str
    path: str
    description: str


class OcrStat(TypedDict):
    label: str
    value: str
    icon: str


class RunningProcess(TypedDict):
    pid: int
    name: str
    cpu: float
    memory: float
    status: Literal["running", "idle", "error"]


class OcrSetting(TypedDict):
    key: str
    value: bool | str | int
    type: Literal["toggle", "text", "number", "select"]
    label: str
    description: str
    options: list[str] | None


class FileItem(TypedDict):
    id: str
    name: str
    icon: str


class ChatMessage(TypedDict):
    role: Literal["user", "assistant"]
    content: str


class LogEntry(TypedDict):
    level: str
    message: str
    timestamp: str


class DocType(TypedDict):
    patterns: list[str]
    priority: int
    steuer_relevant: bool


class Category(TypedDict):
    doc_types: dict[str, DocType]


class Account(TypedDict):
    iban: Optional[str]
    name: str
    bucket: str
    alias: str
    depot_nr: Optional[str]
    verrechnungskonto: Optional[str]
    email: Optional[str]
    bic: Optional[str]


class Company(TypedDict):
    name: str
    aliases: list[str]
    bucket: str
    default_category: str
    accounts: list[Account]


class NamingSchema(TypedDict):
    schema: str
    seq: dict[str, int]
    defaults: dict[str, str]


class UltimateRules(TypedDict):
    version: float
    meta: dict[str, str | bool | list[str]]
    naming: NamingSchema
    companies: dict[str, Company]
    buckets: dict[str, list[str]]
    kategorien: dict[str, dict[str, Category]]


class AppState(rx.State):
    current_page: str = "File Explorer"
    theme: str = "light"
    nav_items: list[NavItem] = [
        {"name": "Dashboard", "icon": "layout-grid", "page": "Dashboard"},
        {"name": "OCR Settings", "icon": "sliders-horizontal", "page": "OCR Settings"},
        {"name": "File Explorer", "icon": "folder-kanban", "page": "File Explorer"},
        {"name": "AI Chat", "icon": "message-circle", "page": "AI Chat"},
        {"name": "AI Renamer Rules", "icon": "sparkles", "page": "AI Rules"},
        {"name": "Company Rules", "icon": "building", "page": "Company Rules"},
        {"name": "Server", "icon": "server", "page": "Server"},
    ]

    @rx.event
    def set_page(self, page_name: str):
        self.current_page = page_name

    @rx.event
    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"


class DashboardState(AppState):
    api_endpoints: list[ApiEndpoint] = [
        {"method": "GET", "path": "/api/status", "description": "Get service status."},
        {"method": "GET", "path": "/api/stats", "description": "Get OCR statistics."},
        {
            "method": "POST",
            "path": "/api/process/file",
            "description": "Process a single file.",
        },
        {"method": "GET", "path": "/api/logs", "description": "Fetch system logs."},
        {
            "method": "GET",
            "path": "/api/config",
            "description": "Retrieve current configuration.",
        },
    ]
    ocr_stats: list[OcrStat] = [
        {"label": "Files Processed", "value": "1,402", "icon": "folder-kanban"},
        {"label": "Total Pages OCR'd", "value": "8,923", "icon": "sliders-horizontal"},
        {"label": "Errors Last 24h", "value": "3", "icon": "server"},
        {"label": "Avg. Process Time", "value": "2.1s", "icon": "timer"},
    ]
    running_processes: list[RunningProcess] = [
        {
            "pid": 101,
            "name": "FastAPI Main Thread",
            "cpu": 5.2,
            "memory": 128.5,
            "status": "running",
        },
        {
            "pid": 205,
            "name": "OCR Watcher Service",
            "cpu": 0.8,
            "memory": 64.2,
            "status": "running",
        },
        {
            "pid": 311,
            "name": "OCR Worker 1",
            "cpu": 89.5,
            "memory": 512.8,
            "status": "running",
        },
        {
            "pid": 312,
            "name": "OCR Worker 2",
            "cpu": 0.1,
            "memory": 256.4,
            "status": "idle",
        },
    ]


class OCRSettingsState(AppState):
    settings: list[OcrSetting] = [
        {
            "key": "skip_text",
            "value": True,
            "type": "toggle",
            "label": "Skip Text",
            "description": "Don't re-process pages with existing text.",
            "options": None,
        },
        {
            "key": "rotate_pages",
            "value": True,
            "type": "toggle",
            "label": "Rotate Pages",
            "description": "Automatically rotate pages based on content.",
            "options": None,
        },
        {
            "key": "deskew",
            "value": True,
            "type": "toggle",
            "label": "Deskew",
            "description": "Correct for skewed or tilted pages.",
            "options": None,
        },
        {
            "key": "clean",
            "value": True,
            "type": "toggle",
            "label": "Clean",
            "description": "Clean background noise from pages.",
            "options": None,
        },
        {
            "key": "clean-final",
            "value": False,
            "type": "toggle",
            "label": "Clean Final",
            "description": "Perform final cleaning operations.",
            "options": None,
        },
        {
            "key": "optimize",
            "value": "2",
            "type": "select",
            "label": "Optimization Level",
            "description": "Balance between quality and file size.",
            "options": ["0", "1", "2", "3"],
        },
        {
            "key": "language",
            "value": "deu+eng",
            "type": "text",
            "label": "Languages",
            "description": "Languages to use for OCR (e.g., 'deu+eng').",
            "options": None,
        },
        {
            "key": "sidecar",
            "value": True,
            "type": "toggle",
            "label": "Create Sidecar File",
            "description": "Create a .txt file with the OCR text.",
            "options": None,
        },
    ]

    @rx.event
    def toggle_setting(self, key: str):
        for i, setting in enumerate(self.settings):
            if setting["key"] == key and setting["type"] == "toggle":
                self.settings[i]["value"] = not self.settings[i]["value"]
                break

    @rx.event
    def set_text_setting(self, key: str, value: str):
        for i, setting in enumerate(self.settings):
            if setting["key"] == key:
                self.settings[i]["value"] = value
                break

    @rx.event
    def save_settings(self):
        yield rx.toast("Settings saved successfully!")


class FileExplorerState(AppState):
    files: list[FileItem] = [
        {"id": "file1", "name": "UIUXMonster.png", "icon": "image"},
        {"id": "file2", "name": "2pacCover.mp3", "icon": "music"},
        {"id": "file3", "name": "UIUXMonster.zip", "icon": "archive"},
        {"id": "file4", "name": "Details.pdf", "icon": "file-text"},
        {"id": "file5", "name": "Better.Call.Saul.S02E10.720p.mp4", "icon": "video"},
        {"id": "file6", "name": "Call Of Duty.apk", "icon": "app-window"},
    ]
    selected_file: str = ""

    @rx.event
    def set_selected_file(self, filename: str):
        self.selected_file = filename


class ServerSettingsState(AppState):
    logs: list[LogEntry] = [
        {
            "level": "INFO",
            "message": "OCR Watcher Service started. Watching /Volumes/DataEX/inbox.",
            "timestamp": "10:30:01",
        },
        {
            "level": "INFO",
            "message": "Detected new file: invoice_2023.pdf",
            "timestamp": "10:30:15",
        },
        {
            "level": "DEBUG",
            "message": "Moving original to archive/invoice_2023.pdf",
            "timestamp": "10:30:15",
        },
        {
            "level": "INFO",
            "message": "Starting OCR process for invoice_2023.pdf [PID: 311]",
            "timestamp": "10:30:16",
        },
        {
            "level": "ERROR",
            "message": "Failed to extract metadata from contract_draft.pdf. Skipping.",
            "timestamp": "10:31:05",
        },
        {
            "level": "INFO",
            "message": "OCR process for invoice_2023.pdf completed in 3.4s.",
            "timestamp": "10:31:19",
        },
    ]


class ChatState(AppState):
    messages: list[ChatMessage] = [
        {
            "role": "assistant",
            "content": "Hello! I am your PDF RAG assistant. How can I help you today?",
        }
    ]
    input_text: str = ""

    @rx.event
    def send_message(self, form_data: dict):
        message = form_data.get("chat_input")
        if not message or not message.strip():
            return
        self.messages.append({"role": "user", "content": message})
        self.messages.append({"role": "assistant", "content": f"Echo: {message}"})