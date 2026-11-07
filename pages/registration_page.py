from __future__ import annotations

import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class RegistrationPage(BasePage):
    FORM = (By.ID, "customerForm")
    SUBMIT = (By.CSS_SELECTOR, "#customerForm input[type='submit']")
    HEADING = (By.CSS_SELECTOR, "#rightPanel h1.title")
    SUCCESS = (By.XPATH, "//div[@id='rightPanel']/p[contains(., 'Your account was created successfully')]")

    @allure.step("Открыть форму регистрации")
    def open(self) -> RegistrationPage:
        self.visit("register.htm")
        self.visible(self.FORM)
        return self

    @allure.step("Заполнить регистрационные данные")
    def fill(self, data: dict[str, str]) -> RegistrationPage:
        for field_id, value in data.items():
            self.enter((By.ID, field_id), value)
        return self

    @allure.step("Отправить регистрационную форму")
    def submit(self) -> RegistrationPage:
        self.click(self.SUBMIT)
        return self

    @allure.step("Проверить успешную регистрацию")
    def expect_account(self, username: str) -> None:
        self.visible(self.SUCCESS)
        assert self.text(self.HEADING) == f"Welcome {username}"

    @allure.step("Проверить сообщение поля {field_id}")
    def expect_validation(self, field_id: str, expected: str) -> None:
        error = (By.ID, f"{field_id}.errors")
        assert self.text(error) == expected
        assert not self.is_displayed(self.SUCCESS), "Форма с ошибкой создала учётную запись"
