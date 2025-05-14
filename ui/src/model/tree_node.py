from pydantic import BaseModel, Field
from typing import Any, Dict, Optional

class TreeNode(BaseModel):
    name: Optional[str] = Field(default=None, description="")
    children: Dict[str, Any] = Field(default={}, description="")
    is_leaf: bool = Field(default=False, description="")

    # def __init__(self, name):
    #     self.name = name
    #     self.children = {}
    #     self.is_leaf = False 