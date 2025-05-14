from pydantic import BaseModel

from typing import List
from ..utils.tools import get_path_depth, get_path_array

class Rule(BaseModel):
    id: str = ""
    generateId: bool = False
    sourcePath: str = ""
    
    targetClass: str = ""
    targetLang: str = ""
    targetProperty: str = ""
    targetFunction: str = ""
    targetValue: str = ""
    targetFunctionParam: str = ""
    
    relationTo: str = ""
    relationName: str = ""
    relationNameInverse: str = ""

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        anystr_strip_whitespace = True

    def __str__(self):
        return f"""
            id : {self.id}
            generateId : {self.generateId}
            sourcePath : {self.sourcePath}
            targetClass : {self.targetClass}
            targetLang : {self.targetLang}
            targetProperty : {self.targetProperty}
            targetFunction : {self.targetFunction}
            targetValue : {self.targetValue}
            targetFunctionParam : {self.targetFunctionParam}
            relationTo : {self.relationTo}
            relationName : {self.relationName}
            relationNameInverse : {self.relationNameInverse}
        """

# class RulesTree(BaseModel):
#     name: str = Field(default="")
#     parent: Optional['RulesTree'] = None
#     depth: int = Field(default=0)
#     children: Dict[str, 'RulesTree'] = Field(default_factory=dict)
#     rules: List[Rule] = Field(default_factory=list)
#     matches: List = Field(default_factory=list)
#     parameters: List = Field(default_factory=list)

class RulesTree:
    def __init__(self) -> None:
        self.name: str = ""
        self.parent = None
        self.children = {}
        self.depth = 0
        self.rules: List[Rule] = []
        self.matches = []
        self.parameters = []

    def add_rule(self, rule: Rule, subPath="") -> None:
        if subPath == "":
            path = rule.sourcePath
        else:
            path = subPath
        depth = get_path_depth(path)
        if depth == 1:
            if path in self.children:
                child = self.children[path]
            else:
                child = RulesTree()
                child.parent = self
                child.depth = self.depth + 1
                child.name = path
                child.children = {}
                self.children[path] = child
                child.rules = []
            child.rules.append(rule)
        else:
            path_array = get_path_array(path)
            path = path_array[0]
            depth = get_path_depth(path)
            if path in self.children:
                child = self.children[path]
            else:
                child = RulesTree()
                child.parent = self
                child.depth = self.depth + 1
                child.name = path
                child.children = {}
                self.children[path] = child
                child.rules = []
            if child.name == path_array[len(path_array) - 1]:
                child.rules.append(rule)
            path_array.remove(path)
            if not len(path_array) == 0:
                currentPath = ".".join([path for path in path_array])
                child.add_rule(rule, currentPath)

    def display(self):
        return "\t" * (self.depth - 1) + self.name
    
    def display_all(self):
        def traverse(node: RulesTree):
            node_data = vars(node)
            tabs = "\t" * (node_data["depth"] - 1)
            result = ""
            if node_data["depth"] != 0:
                result = f'{tabs}{node_data["name"]}\n'
            for child in node_data["children"].values():
                result += traverse(child)
            return result
        result = traverse(self)
        return result
        