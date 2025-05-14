class Rule:
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
