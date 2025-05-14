from fastapi import Depends
from typing_extensions import Annotated
from .service import RuleService
from ..user.model import User
from ..auth.dependencies import get_current_user

def get_rule_service(current_user: User = Depends(get_current_user)) -> RuleService:
    return RuleService(current_user)

RuleServiceDep = Annotated[RuleService, Depends(get_rule_service)]
