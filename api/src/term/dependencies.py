from fastapi import Depends
from typing_extensions import Annotated
from .service import TermService
from ..user.model import User
from ..auth.dependencies import get_current_user

def get_term_service(current_user: User = Depends(get_current_user)) -> TermService:
    return TermService(current_user)

TermServiceDep = Annotated[TermService, Depends(get_term_service)]
