# UI-тесты регистрации ParaBank

Проект для воркшопа по веб-тестированию. Проверки запускаются в Chrome и Firefox на Selenium и pytest. Allure сохраняет шаги сценариев и диагностику падений.

## Сценарии

| Ввод | Ожидаемый результат |
| --- | --- |
| Валидные данные с уникальным логином | Сообщение об успешной регистрации и логин в заголовке |
| Пустая фамилия | Last name is required. |
| Пустой адрес | Address is required. |
| Пустой город | City is required. |
| Пустой почтовый индекс | Zip Code is required. |
| Пустое подтверждение пароля | Password confirmation is required. |
| Пароль и подтверждение различаются | Passwords did not match. |

## Запуск

Установите Python 3.12 и браузеры Chrome и Firefox. Selenium Manager подбирает драйверы при первом запуске. Команды для PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest
```

Обычный запуск проверяет все семь сценариев в обоих браузерах. Опция `--browser=chrome` или `--browser=firefox` выбирает один браузер. Опция `--headed` открывает окно. Маркер `-m smoke` выбирает успешную регистрацию, а `-m validation` выбирает проверки формы.

По умолчанию используется [демонстрационный стенд ParaBank](https://parabank.parasoft.com/parabank/register.htm). Для запуска на своём стенде передайте базовый адрес с контекстом `/parabank` через `--base-url` или переменную `PARABANK_URL`.

## Устройство проекта

- `pages/base_page.py` содержит явные ожидания и базовые действия Selenium.
- `pages/registration_page.py` содержит локаторы и методы формы. Методы `open`, `fill` и `submit` возвращают страницу для цепочки вызовов.
- `conftest.py` задаёт адрес, тестовые данные и жизненный цикл браузера. Неявное ожидание равно нулю.
- `diagnostics.py` записывает консоль и HTTP-события через WebDriver BiDi в обоих браузерах.
- `tests/test_registration.py` содержит позитивную проверку и шесть негативных случаев.

## Отчёт Allure

`pytest.ini` сохраняет результаты в `allure-results`. Откройте их через установленный [Allure CLI](https://allurereport.org/docs/pytest/):

```powershell
allure serve allure-results
```

При падении фикстура прикладывает снимок экрана, журнал консоли и журнал сетевых запросов до закрытия браузера. Сетевой журнал содержит HTTP-методы, адреса без параметров и коды ответов. Данные формы синтетические.

## Результат проверки

На локальном экземпляре ParaBank прошли 7 проверок в Chrome и 7 в Firefox. При контрольном падении в каждом браузере Allure сохранил все три вложения. Публичный стенд вернул HTTP 403 из среды проверки. [Образ ParaBank от Parasoft](https://hub.docker.com/r/parasoft/parabank)
