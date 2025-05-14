from fastapi.security import OAuth2PasswordRequestFormStrict
from typing_extensions import Annotated
from fastapi import Depends, HTTPException, status
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from .model import Token
from .dependencies import AuthServiceDep

router = InferringRouter(tags=["auth"], prefix="/auth")

@cbv(router)
class AuthController:
    
    def __init__(self, auth_service: AuthServiceDep) -> None:
        self.auth_service = auth_service

    @router.post("/token")
    async def login_for_access_token(
        self,
        form_data: Annotated[OAuth2PasswordRequestFormStrict, Depends()],
    ) -> Token:
        access_token = await self.auth_service.authenticate(form_data.username, form_data.password)
        
        if not isinstance(access_token, Token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized access",
                headers={"WWW-Authenticate": "Bearer"},
            )
       
        return access_token