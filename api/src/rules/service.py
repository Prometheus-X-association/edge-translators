from copy import deepcopy
from datetime import datetime
from typing import Any, Dict, List, Literal, Mapping
from elasticsearch import NotFoundError
from jsonpath_ng.ext import parse
from ..elasticsearch.client import ElasticsearchClient
from .model import RulesTree, Rule
from ..utils.tools import get_path_array, get_path_depth
from ..user.model import User
from slugify import slugify 

class RuleService:
    
    ELASTICSEARCH_INDEX_RULES = "edge_rules"

    def __init__(self, current_user: User) -> None:
        self.current_user = current_user
        self.es_client = ElasticsearchClient().client
        self.counters: dict[str, int] = {}
        self.instances: dict[str, dict] = {}
        self.rules_tree: RulesTree = None
    
    def find(self) -> Dict[str, List[Dict]]|None:
        id = self.set_id()
        try:
            response = self.es_client.get(index=self.ELASTICSEARCH_INDEX_RULES, id=id)

            if response == None or "_source" not in response:
                return None
            return response["_source"]
        except NotFoundError as e:
            return None
        except Exception as e:
            raise Exception(f"Error: {e}")

    def upsert(self, payload: Mapping[str, Any], refresh=None) -> None:
        id = self.set_id()
        self.es_client.index(index=self.ELASTICSEARCH_INDEX_RULES, document=payload, id=id, refresh=refresh)

    def delete(self, refresh=None) -> None:
        id = self.set_id()
        try:
            self.es_client.delete(index=self.ELASTICSEARCH_INDEX_RULES, id=id, refresh=refresh)
        except NotFoundError as e:
           return
    
    def apply(self, documents: List[dict]) -> dict | Literal[False]:
        response = self.find()
        if response == None:
            return False

        rules: List[Rule] = [Rule(**val) for val in response["graph"]]

        if not isinstance(rules, list) or not all(isinstance(rule, Rule) for rule in rules):
            raise Exception("rules must be a list of Rule objects")
        
        rules_copy = deepcopy(rules)
        self.rules_tree = self.generate_rules_tree(provider_rules=rules_copy)

        serialisation = {}

        serialisation["@context"] = "https://mindmatcher.org/ontology-1.0.0.jsonld"
        result = []
        docIndex = 0

        if isinstance(documents, dict):
            documents = [documents]
        for document in documents:
            self.apply_tree_rules_to_document(document, docIndex)
            docIndex = docIndex + 1

        for instance in self.instances.values():
            del instance["__counter__"]
            result.append(instance)

        serialisation["graph"] = result
        return serialisation

    @staticmethod
    def browse_rules_tree(root: RulesTree) -> List[RulesTree]:
        if not root:
            return []
    
        res = [root]
        for child in root.children.values():
            res.extend(RuleService.browse_rules_tree(child))
    
        return res

    @staticmethod
    def display_rules_tree(rules_tree: RulesTree) -> str:
        rules = RuleService.browse_rules_tree(rules_tree)
        return "\n".join([rule.display() for rule in rules if rule.depth != 0])

    @staticmethod
    def generate_rules_tree(provider_rules: List[Rule]) -> RulesTree:
        rulesByDepth: dict[int, List[Rule]] = {}
        for rule in provider_rules:
            depth = get_path_depth(rule.sourcePath)
            if not depth in rulesByDepth:
                rulesByDepth[depth] = []
            rulesByDepth[depth].append(rule)
        
        orderedDepth = sorted(rulesByDepth)
        documentTree = RulesTree()
        documentTree.name = "root"
        for depth in orderedDepth:
            for rule in rulesByDepth[depth]:
                documentTree.add_rule(rule)
        
        return documentTree

    def set_id(self) -> str:
        return f"rule:provider/{self.current_user.username}"

    def generate_id(self, instance: dict, value: str) -> str:
        object = instance["type"].replace("soo:", "").lower()
        return f"{object}:provider/{slugify(self.current_user.username)}/value/{slugify(value)}"

    def check_instance(self, targetClass: str, docIndex: int, index: int):
        if index == -1:
            key = f"{docIndex}-{targetClass}"
        else:
            key = f"{docIndex}-{targetClass}-{index}"
        return any([x for x in self.instances if key.lower() in x.lower()])

    def get_last_instance(self, targetClass: str, docIndex: int, index: int):
        if not self.check_instance(targetClass, docIndex, index):
            return None
        if index == -1:
            key = f"{docIndex}-{targetClass}"
        else:
            key = f"{docIndex}-{targetClass}-{index}"
        keys = [x for x in reversed(self.instances) if key.lower() in x.lower()]
        return self.instances[keys[0]]

    def get_instance(self, targetClass: str, index: int, docIndex: int, prefix: str = "") -> dict:
        key = f"{docIndex}-{targetClass}-{index}-{prefix}"
        if not targetClass in self.counters.keys():
            self.counters[targetClass] = 0
        currentInstance = None
        if key in self.instances.keys():
            return self.instances[key]

        self.counters[targetClass] = self.counters[targetClass] + 1
        currentInstance = {}
        currentInstance["type"] = targetClass
        currentInstance["__counter__"] = self.counters[targetClass]
        self.instances[key] = currentInstance
        return currentInstance

    def get_documents_from_files(self, file: dict) -> List[dict]:
        documents = []
        sourcepaths: dict[int, List[str]] = {}
        depth = 0
        response = self.find()

        if response is None:
            raise Exception()

        for rule in response["rules"]:
            if isinstance(rule, str):
                continue
            if not rule.sourcePath in sourcepaths:
                split_path = rule.sourcePath.split(".")
                depth_path = len(split_path)
                if not depth_path in sourcepaths:
                    sourcepaths[depth_path] = []
                sourcepaths[depth_path].append(rule.sourcePath)

        orderDepths = sorted(sourcepaths)
        numberOfDocuments = 0
        for depth in orderDepths:
            filedValues = {}
            for sourcepath in sourcepaths[depth]:
                # [*].'Date'
                jsonpath = ""
                for source_path_element in sourcepath.split("."):
                    jsonpath = jsonpath + "[*].'" + source_path_element + "'"
                jsonPath_expression = parse(jsonpath)
                matches = jsonPath_expression.find(file)
                filedValues[sourcepath] = []
                numberOfDocuments = max(numberOfDocuments, len(matches))
                for match in matches:
                    filedValues[sourcepath].append(match.value)

        for i in range(0, numberOfDocuments):
            document = {}
            for key in filedValues.keys():
                document[key] = filedValues[key][i]
            documents.append(document)
        return documents

    def get_field_name(self, field: str) -> str:
        return field.replace("soo:has", "").replace("soo:", "").replace("skos:", "")

    def fill_with_document(self, file: dict) -> None:
        self.rules_tree.matches = []
        self.rules_tree.matches.append(file)
        rules_trees = self.browse_rules_tree(self.rules_tree)
        i = 0
        for rules_tree in rules_trees:
            if rules_tree.depth == 0:
                continue

            # add matches in file to rule.
            jsonpath = "[*].'" + rules_tree.name + "'"
            jsonPath_expression = parse(jsonpath)
            rules_tree.matches = []
            rules_tree.parameters = []

            for match in rules_tree.parent.matches:
                current_matches = jsonPath_expression.find(match)
                for current_match in current_matches:
                    rules_tree.matches.append(current_match.value)
                for rule in rules_tree.rules:
                    if rule.targetFunctionParam != "" and "fno:" not in rule.targetFunctionParam:
                        path_array = get_path_array(rule.targetFunctionParam)
                        jsonpath_par = "[*].'" + path_array[len(path_array) - 1] + "'"
                        jsonPath_expression_par = parse(jsonpath_par)
                        current_matches_par = jsonPath_expression_par.find(match)
                        for current_match_par in current_matches_par:
                            rules_tree.parameters.append(current_match_par.value)
                        break

    def generate_instances_by_tree(self, filed_rules_tree: RulesTree, docIndex: int) -> None:
        rules_trees = self.browse_rules_tree(filed_rules_tree)
        lag_rules = []
        i = 1
        for rule_tree in rules_trees:
            if rule_tree.depth == 0:
                continue
            if len(rule_tree.rules) == 0:
                continue
            if rule_tree.parent == None:
                prefix = ""
            else:
                prefix = rule_tree.parent.name
            
            # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            # print("rule_tree.rules", rule_tree.rules)
            # print("rule_tree.matches", rule_tree.matches)
            # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            for rule in rule_tree.rules:
                if len(rule_tree.matches) == 0 : 
                    print('## Log:', 'This rule do not match any Node in source file:', rule)
                for index, match in enumerate(rule_tree.matches):
                    currentInstance = self.get_instance(rule.targetClass, index, docIndex, prefix)

                    target = self.get_field_name(rule.targetProperty)
                    if (rule.targetProperty == "id" and rule.targetFunction == "fno:generateId") or rule.generateId == True:
                        currentInstance["id"] = self.generate_id(currentInstance, match)
                        if rule.targetProperty == "id":
                            continue
                    # print("cccccccccccccccccccccccccccccccccccccc")
                    # print(lag_rules)

                    for lag_rule in lag_rules:
                        # print("lag_rule", lag_rule)
                        # print("rule", rule)
                        currentInstanceFrom = self.get_last_instance(lag_rule.relationNameInverse, docIndex, -1)
                        if (currentInstanceFrom != None and currentInstanceFrom["type"] != currentInstance["type"] and currentInstance["type"] == lag_rule.relationTo):
                            if not currentInstanceFrom == None:
                                if self.get_field_name(lag_rule.relationTo).lower() in currentInstanceFrom:
                                    if isinstance(currentInstanceFrom[self.get_field_name(lag_rule.relationTo).lower()], str):
                                        prevRef = str(currentInstanceFrom[self.get_field_name(lag_rule.relationTo).lower()])
                                        currentInstanceFrom[self.get_field_name(lag_rule.relationTo).lower()] = []
                                        currentInstanceFrom[self.get_field_name(lag_rule.relationTo).lower()].append(prevRef)
                                    if (not currentInstance["id"] in currentInstanceFrom[self.get_field_name(lag_rule.relationTo).lower()]):
                                        currentInstanceFrom[self.get_field_name(lag_rule.relationTo).lower()].append(currentInstance["id"])
                                else:
                                    currentInstanceFrom[self.get_field_name(lag_rule.relationTo).lower()] = currentInstance["id"]

                    if rule.targetFunction == "fno:date-to-xsd":
                        dates = match
                        # print(f"--------------------------")
                        # print(f"Iteration : {i}")
                        # print(f"rule : {rule.id}")
                        # print(f"index : {index}")
                        # print(f"match : {match}")
                        if rule.targetFunctionParam == "param:year-only":
                            date = datetime.strptime(f"{match}-01-01", "%Y-%m-%d")
                        else:
                            date = datetime.strptime(dates, "%Y-%m-%d")
                        currentInstance[target] = date.strftime("%Y-%m-%d")
                        continue

                    if rule.relationTo != "" and rule.relationName != "" and rule.relationNameInverse != "":
                        # print(f"--------------------------")
                        # print(f"Iteration : {i}")
                        # print(f"rule : {rule.id}")
                        # print(f"index : {index}")
                        # print(f"match : {match}")
                        i += 1
                        # same cardinality : ex polarity with orientoi : 1 polarity by experience
                        currentInstanceTo = self.get_last_instance(rule.relationTo, docIndex, index)
                        if currentInstanceTo == None: 
                            # different cardinality : ex skill with pitango : 1 experience with many skills
                            currentInstanceTo = self.get_last_instance(rule.relationTo, docIndex, -1)
                        
                        if not currentInstanceTo == None:
                            if self.get_field_name(rule.relationNameInverse).lower() in currentInstanceTo:
                                if isinstance(currentInstanceTo[self.get_field_name(rule.relationNameInverse).lower()], str):
                                    
                                    prevRef = currentInstanceTo[self.get_field_name(rule.relationNameInverse).lower()]
                                    currentInstanceTo[self.get_field_name(rule.relationNameInverse).lower()] = []
                                    currentInstanceTo[self.get_field_name(rule.relationNameInverse).lower()].append(prevRef)
                                
                                currentInstanceTo[self.get_field_name(rule.relationNameInverse).lower()].append(currentInstance["id"])
                            else:
                                currentInstanceTo[self.get_field_name(rule.relationNameInverse).lower()] = currentInstance["id"]
                            currentInstance[self.get_field_name(rule.relationTo).lower()] = currentInstanceTo["id"]
                        else:
                            # Relation does not exist : needs to apply lag rule ( reference to an instance created later)
                            lag_rules.append(rule)
                            pass

                    if rule.targetFunction == "fno:asIs_WithLang":
                        currentInstance[target] = {}
                        currentInstance[target]["@value"] = match
                        currentInstance[target]["@language"] = rule.targetLang if rule.targetLang != "" else "en"
                        continue

                    if rule.targetFunction == "fno:find-matching":
                        currentInstance["__matching__"] = {}
                        currentInstance["__matching__"]["sourceValue"] = match
                        if len(rule_tree.parameters) > 0:
                            currentInstance["__matching__"]["parameter"] = rule_tree.parameters[index]
                        currentInstance["__matching__"]["provider"] = self.current_user.username

                        if "skill" in str.lower(currentInstance["type"]):
                            currentInstance["__matching__"]["subtype"] = "skill"
                        else:
                            currentInstance["__matching__"]["subtype"] = "job"
                        currentInstance["__matching__"]["language"] = rule.targetLang if rule.targetLang != "" else "en"
                        continue

                    if rule.targetFunction == "fno:handle-family":
                        currentInstance["__family__"] = {}
                        fieldName = self.get_field_name(rule.targetProperty)
                        currentInstance["__family__"]["str_value"] = str(match)
                        currentInstance["__family__"]["scale_path"] = rule.sourcePath
                        currentInstance["__family__"]["targetFunction"] = rule.targetFunction
                        currentInstance["__family__"]["value"] = match
                        currentInstance["__family__"]["scale"] = fieldName
                        currentInstance["__family__"]["provider"] = self.current_user.username
                        continue

                    if rule.targetFunction == "fno:skill-value-to-scale" or rule.targetFunction == "fno:find-or-create-term" or rule.targetFunction == "fno:handle-polarity":
                        currentInstance["__term__"] = {}
                        fieldName = self.get_field_name(rule.targetClass)
                        currentInstance["__term__"]["str_value"] = str(match)
                        currentInstance["__term__"]["scale_path"] = rule.sourcePath
                        currentInstance["__term__"]["targetFunction"] = rule.targetFunction
                        currentInstance["__term__"]["value"] = match
                        currentInstance["__term__"]["scale"] = fieldName
                        currentInstance["__term__"]["provider"] = self.current_user.username
                        continue

                    if rule.targetValue != "":
                        currentInstance[target] = rule.targetValue
                        continue
                    if target != "":
                        currentInstance[target] = match
        pass

    def apply_tree_rules_to_document(self, document: dict, docIndex: int):
        self.fill_with_document(document)
        self.generate_instances_by_tree(self.rules_tree, docIndex)
