import logging
from fastapi import Depends, FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from .auth.router import router as auth_router
from .user.router import router as user_router
from .rules.router import router as rule_router
from .matching.router import router as matching_router
from .transform.router import router as transform_router
from .auth.dependencies import oauth2_scheme
from .config import openapi_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_app():
    app = FastAPI(**openapi_settings)
    
    app.include_router(auth_router)
    app.include_router(user_router, dependencies=[Depends(oauth2_scheme)])
    app.include_router(rule_router, dependencies=[Depends(oauth2_scheme)])
    app.include_router(matching_router, dependencies=[Depends(oauth2_scheme)])
    app.include_router(transform_router, dependencies=[Depends(oauth2_scheme)])
    
    return app

app = get_app()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

@app.get(
    "/health",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    include_in_schema=False
)
def get_health() -> Response:
    return Response("ok", status.HTTP_200_OK)

