from __future__ import annotations

import allure
from selenium.webdriver.support import expected_conditions as conditions
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    @allure.step("Настроить явные ожидания")
    def __init__(self, driver, base_url: str):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, timeout=10, poll_frequency=0.2)

    @allure.step("Открыть страницу {path}")
    def visit(self, path: str) -> None:
        self.driver.get(f"{self.base_url}/{path}")

    @allure.step("Дождаться видимости элемента {locator}")
    def visible(self, locator):
        return self.wait.until(
            conditions.visibility_of_element_located(locator),
            message=f"Элемент {locator!r} не стал видимым",
        )

    @allure.step("Заполнить поле {locator}")
    def enter(self, locator, value: str) -> None:
        element = self.visible(locator)
        element.clear()
        if value:
            element.send_keys(value)

    @allure.step("Нажать элемент {locator}")
    def click(self, locator) -> None:
        element = self.wait.until(
            conditions.element_to_be_clickable(locator),
            message=f"Элемент {locator!r} не стал доступен для нажатия",
        )
        element.click()

    @allure.step("Прочитать текст элемента {locator}")
    def text(self, locator) -> str:
        return self.visible(locator).text.strip()

    @allure.step("Проверить текущее состояние элемента {locator}")
    def is_displayed(self, locator) -> bool:
        return any(element.is_displayed() for element in self.driver.find_elements(*locator))
