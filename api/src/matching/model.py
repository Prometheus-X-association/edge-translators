from pydantic import BaseModel, Field
from typing import List, Dict, Any

class PrefLabel(BaseModel):
    value: str = Field(default="", description="The label's value")
    language: str = Field(default="", description="The language of the label")

class Suggestion(BaseModel):
    id: str = Field(..., description="")
    type: str = Field(..., description="")
    target: Dict[str, Any] = Field(..., description="")
    score: float = Field(..., description="")
    validated: int = Field(0, description="")
    framework: str = Field(..., description="")
    mappingType: str = Field(..., description="")


class Matching(BaseModel):
    id: str = Field(..., description="")
    prefLabel: PrefLabel
    description: str = Field(..., description="")
    type: str = Field(..., description="")
    framework: str = Field(..., description="")
    provider: str = Field(..., description="")
    match: Suggestion | None
    suggestions: List[Suggestion]