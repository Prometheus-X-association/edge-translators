from typing import Literal
from fastapi import Body, Query, HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from .model import TransformConfig
from ..rules.dependencies import RuleServiceDep
from ..term.dependencies import TermServiceDep
from ..matching.dependencies import MatchingServiceDep

router = InferringRouter(tags=['transform'])

@cbv(router)
class TransformController:
    def __init__(
        self,
        rule_service: RuleServiceDep,
        term_service: TermServiceDep,
        matching_service: MatchingServiceDep,
    ) -> None:
        self.rule_service = rule_service
        self.term_service = term_service
        self.matching_service = matching_service

    @router.post("/transform")
    async def transform(
        self,
        document: list[dict] | dict = Body(..., description="the document", embed=True),
        target_framework: Literal["esco", "rome"] = Query(default="esco"),
        language_source: Literal["en","fr","fi","es","de"] = Query(default="fr"),
        language_target: Literal["en","fr","fi","es","de"] = Query(default="fr"),
    ):
        if isinstance(document, dict):
            document = [document]
        
        if self.rule_service.find() == None:
            raise HTTPException(status_code=404, detail="Missing rules")
        
        generated_data = self.rule_service.apply(document)

        self.term_service.generate(documents=generated_data)

        transform_config = TransformConfig(
            framework=target_framework,
            language_source=language_source,
            language_target=language_target
        )
        self.matching_service.generate(documents=generated_data, transform_config=transform_config)


        return generated_data