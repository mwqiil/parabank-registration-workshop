"""Запись консоли и сетевых событий через WebDriver BiDi."""

from collections import deque
from urllib.parse import urlsplit, urlunsplit


def _http_url(url: str) -> str | None:
    parts = urlsplit(url)
    if parts.scheme not in {"http", "https"}:
        return None
    return urlunsplit((parts.scheme, parts.netloc.rsplit("@", 1)[-1], parts.path, "", ""))


def record_browser_events(driver):
    console = deque(maxlen=250)
    network = deque(maxlen=250)

    def record_console(entry):
        console.append({"level": entry.level, "message": entry.text})

    def record_script_error(entry):
        console.append({"level": "error", "message": entry.message})

    def record_request(event):
        request = event["request"] if isinstance(event, dict) else event.request
        url = _http_url(request["url"])
        if url:
            network.append({
                "event": "request",
                "id": request["request"],
                "method": request["method"],
                "url": url,
            })

    def record_response(event):
        response = event["response"] if isinstance(event, dict) else event.response
        request = event["request"] if isinstance(event, dict) else event.request
        url = _http_url(response["url"])
        if url:
            network.append({
                "event": "response",
                "id": request["request"],
                "status": response["status"],
                "url": url,
            })

    driver.script.add_console_handler(record_console)
    driver.script.add_error_handler(record_script_error)
    driver.network.add_event_handler("before_request_sent", record_request)
    driver.network.add_event_handler("response_completed", record_response)
    return console, network
