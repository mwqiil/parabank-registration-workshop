import allure
import pytest

from pages.registration_page import RegistrationPage


@pytest.mark.smoke
@allure.title("Регистрация с валидными данными")
def test_register_account(driver, base_url, registration_data):
    (
        RegistrationPage(driver, base_url)
        .open()
        .fill(registration_data)
        .submit()
        .expect_account(registration_data["customer.username"])
    )


@pytest.mark.validation
@allure.title("Проверка обязательного поля [{param_id}]")
@pytest.mark.parametrize(
    ("field_id", "message"),
    [
        pytest.param("customer.lastName", "Last name is required.", id="last-name"),
        pytest.param("customer.address.street", "Address is required.", id="street"),
        pytest.param("customer.address.city", "City is required.", id="city"),
        pytest.param("customer.address.zipCode", "Zip Code is required.", id="zip-code"),
        pytest.param("repeatedPassword", "Password confirmation is required.", id="confirmation"),
    ],
)
def test_required_field(driver, base_url, registration_data, field_id, message):
    (
        RegistrationPage(driver, base_url)
        .open()
        .fill(registration_data | {field_id: ""})
        .submit()
        .expect_validation(field_id, message)
    )


@pytest.mark.validation
@allure.title("Подтверждение не совпадает с паролем")
def test_password_confirmation_mismatch(driver, base_url, registration_data):
    (
        RegistrationPage(driver, base_url)
        .open()
        .fill(registration_data | {"repeatedPassword": "OtherSample2026!"})
        .submit()
        .expect_validation("repeatedPassword", "Passwords did not match.")
    )
