from typing import Any
from fastapi import Body, HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from .dependencies import RuleServiceDep

router = InferringRouter(tags=["rules"])

@cbv(router)
class RuleController:
    
    def __init__(self, rule_service: RuleServiceDep) -> None:
        self.rule_service = rule_service

    @router.get("/rules")
    async def get_rules(self) -> Any:
        rules = self.rule_service.find()

        if rules is None:
            raise HTTPException(status_code=404, detail="Missing rules")
        
        return rules

    @router.post("/rules")
    async def post_rules(self, rules: dict = Body(..., description="The provider rules", embed=True)) -> dict:
        self.rule_service.upsert(payload=rules)
        return { "response": "ok" }
