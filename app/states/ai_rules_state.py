import reflex as rx
from app.state import UltimateRules, AppState
import yaml
import logging
from typing import TypedDict


class AIDocType(TypedDict):
    name: str
    patterns: list[str]
    priority: int
    steuer_relevant: bool


class AISubKategorie(TypedDict):
    name: str
    doc_types: list[AIDocType]


class AIKategorie(TypedDict):
    name: str
    sub_categories: list[AISubKategorie]


class AIRulesState(AppState):
    rules: UltimateRules = {}
    kategorien_list: list[AIKategorie] = []

    def _load_rules(self):
        if not self.rules:
            try:
                with open("assets/ultimate_rules.yaml", "r", encoding="utf-8") as f:
                    self.rules = yaml.safe_load(f)
                    self._structure_kategorien()
            except FileNotFoundError as e:
                logging.exception(f"Error: {e}")
                print("ultimate_rules.yaml not found")
                self.rules = {}

    def _structure_kategorien(self):
        self.kategorien_list = []
        if "kategorien" in self.rules:
            for main_cat, sub_cats in self.rules["kategorien"].items():
                sub_list = []
                for sub_cat, details in sub_cats.items():
                    doc_types_list = []
                    if "doc_types" in details:
                        for doc_name, doc_details in details["doc_types"].items():
                            doc_types_list.append(
                                {
                                    "name": doc_name,
                                    "patterns": doc_details.get("patterns", []),
                                    "priority": doc_details.get("priority", 0),
                                    "steuer_relevant": doc_details.get(
                                        "steuer_relevant", False
                                    ),
                                }
                            )
                    sub_list.append({"name": sub_cat, "doc_types": doc_types_list})
                self.kategorien_list.append(
                    {"name": main_cat, "sub_categories": sub_list}
                )

    @rx.event
    def on_load(self):
        self._load_rules()

    @rx.event
    def save_rules(self):
        try:
            with open("assets/ultimate_rules.yaml", "w", encoding="utf-8") as f:
                yaml.dump(self.rules, f, allow_unicode=True, sort_keys=False)
            yield rx.toast.success("AI rules saved successfully!")
        except Exception as e:
            logging.exception(f"Error saving AI rules: {e}")
            yield rx.toast.error("Failed to save AI rules.")