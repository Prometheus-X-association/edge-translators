import requests

from ..config import settings

class EscoHelperClient:

    def __init__(self):
        self.client = requests
        self.base_url = settings.esco_helper_url

    def translate_label(
            self,
            uri: str,
            target_language: str
    ) -> str:
        url: str = f"{self.base_url}/api/v1/esco/getLabel"
        payload: dict[str, str] = {"language": target_language, "uri": uri}

        try:
            response = self.client.post(
                url,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            
            data = response.json()
            return data.get("label", "Label not found")
        except requests.exceptions.Timeout:
            raise
        except requests.exceptions.ConnectionError:
            raise
        except requests.exceptions.HTTPError as http_err:
            raise
        except requests.exceptions.RequestException as req_err:
            raise
