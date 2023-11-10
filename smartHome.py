from homeassistant_api import Client

class SmartHome:
    def __init__(self, hass_api_url:str, hass_token:str):
        self.hass_api_url = hass_api_url
        self.hass_token = hass_token

    def turn_on(self, entity_id:str):
        with Client(
            self.hass_api_url,
            self.hass_token,
        ) as client:
            light = client.get_domain("light")
            light.turn_on(entity_id=entity_id)
    