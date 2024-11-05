import requests
import pytest

user_agents = [
    ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36", "Unknown", "Chrome", "Web"),
    ("Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15A5341f Safari/604.1", "iOS", "Unknown", "Mobile"),
]

@pytest.mark.parametrize("user_agent, expected_device, expected_browser, expected_platform", user_agents)
def test_user_agent_check(user_agent, expected_device, expected_browser, expected_platform):
    response = requests.get(
        "https://playground.learnqa.ru/ajax/api/user_agent_check",
        headers={"User-Agent": user_agent}
    )

    response_data = response.json()
    errors = []

    if response_data["device"] != expected_device:
        errors.append(f"device: expected {expected_device}, got {response_data['device']}")
    if response_data["browser"] != expected_browser:
        errors.append(f"browser: expected {expected_browser}, got {response_data['browser']}")
    if response_data["platform"] != expected_platform:
        errors.append(f"platform: expected {expected_platform}, got {response_data['platform']}")

    assert not errors, f"User Agent '{user_agent}' вернул ошибки: " + "; ".join(errors)
