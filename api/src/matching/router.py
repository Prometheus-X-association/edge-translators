from typing import Any, Optional, Literal
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi.param_functions import Query
from .dependencies import MatchingServiceDep

router = InferringRouter(tags=["matching"])

@cbv(router)
class MatchingController:
    
    def __init__(self, matching_service: MatchingServiceDep) -> None:
        self.matching_service = matching_service

    @router.get("/matching")
    async def get_matching(
        self,
        validated: Optional[bool]|None = Query(default=None, description=""),
        concept_type: Optional[Literal["experience", "skill"]] = Query(default="experience"),
        framework: Optional[Literal["esco", "rome"]] = Query(default="esco"),
    ) -> Any:
        response = self.matching_service.find_some(
            validated = validated,
            concept_type = f"soo:{concept_type.capitalize()}",
            framework = framework
        )

        return response

    @router.delete("/matching")
    async def delete_all(self) -> bool:
        self.matching_service.delete_all()

        return True
    