import pytest

from ..smartHome import SmartHome

@pytest.fixture
def smarthome():
    return SmartHome("http://localhost:8123", "abc")

# def test_init(smarthome):
#     assert smarthome.hass_api_url == "http://localhost:8123"
#     assert smarthome.hass_token == "abc"

