# allow to load the .env file as a singleton for environment variables
from enum import auto
from functools import lru_cache
from fastapi_utils.enums import StrEnum
from fastapi_utils.api_settings import APISettings


class Environment(StrEnum):
    dev = auto()
    prod = auto()
    test = auto()    

class Settings(APISettings):
    environment: Environment = Environment.prod
    esco_helper_url: str
    indice_mapping: str
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: str
    class Config(APISettings.Config):
        env_file = ".env"

@lru_cache()
def get_api_settings() -> Settings:
    return Settings()



settings = get_api_settings()


openapi_settings = {}
openapi_settings["title"] = "Onto-Terminology AI Translator API"
openapi_settings["version"] = "1.0.0"
openapi_settings["docs_url"] = "/docs"
openapi_settings["debug"] = True
openapi_settings["openapi_prefix"] = ""
openapi_settings["openapi_url"] = "/openapi.json"
openapi_settings["redoc_url"] = "/redoc"
openapi_settings["summary"] = "Onto-Terminology AI Translator API"
openapi_settings["description"] = ""
openapi_settings["disable_docs"] = False
openapi_settings["openapi_tags"] = [
    {
        "name": "rules",
        "description": "Operations with **rules**.",
    },{
        "name": "transform",
        "description": "Operations with **transform**.",
    }
]