import reflex as rx
from app.state import UltimateRules, Company, AppState
import yaml
import logging
from typing import cast


class CompanyRulesState(AppState):
    rules: UltimateRules = {}
    companies_list: list[Company] = []
    selected_company: Company | None = None

    def _load_rules(self):
        if not self.rules:
            try:
                with open("assets/ultimate_rules.yaml", "r", encoding="utf-8") as f:
                    self.rules = yaml.safe_load(f)
                    self._structure_companies()
            except FileNotFoundError as e:
                logging.exception(f"Error: {e}")
                print("ultimate_rules.yaml not found")
                self.rules = {}

    def _structure_companies(self):
        self.companies_list = []
        if "companies" in self.rules:
            for company_name, details in self.rules["companies"].items():
                company_data = {"name": company_name, **details}
                if "accounts" not in company_data:
                    company_data["accounts"] = []
                self.companies_list.append(cast(Company, company_data))

    @rx.event
    def on_load(self):
        self._load_rules()

    @rx.event
    def save_rules(self):
        if not self.rules:
            return
        companies_dict = {comp["name"]: comp for comp in self.companies_list}
        for comp in self.companies_list:
            company_data = dict(comp)
            del company_data["name"]
            companies_dict[comp["name"]] = company_data
        self.rules["companies"] = companies_dict
        try:
            with open("assets/ultimate_rules.yaml", "w", encoding="utf-8") as f:
                yaml.dump(self.rules, f, allow_unicode=True, sort_keys=False)
            yield rx.toast.success("Company rules saved successfully!")
        except Exception as e:
            logging.exception(f"Error saving company rules: {e}")
            yield rx.toast.error("Failed to save company rules.")

    @rx.event
    def select_company(self, company_name: str):
        for company in self.companies_list:
            if company["name"] == company_name:
                self.selected_company = company
                break