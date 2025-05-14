

from typing import Literal
from pydantic import BaseModel, Field


class TransformConfig(BaseModel):
    framework: Literal["esco", "rome"] = Field(default="esco", description="The framework used")
    language_source: Literal["en","fr","fi","es","de"] = Field(default="fr", description="The source language")
    language_target: Literal["en","fr","fi","es","de"] = Field(default="en", description="The target language")   
