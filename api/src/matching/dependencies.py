from fastapi import Depends
from typing_extensions import Annotated
from .service import MatchingService
from ..user.model import User
from ..auth.dependencies import get_current_user

def get_matching_service(current_user: User = Depends(get_current_user)) -> MatchingService:
    matching_service = MatchingService(current_user)
    return matching_service

MatchingServiceDep = Annotated[MatchingService, Depends(get_matching_service)]
