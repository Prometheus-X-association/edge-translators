from pydantic import BaseModel, Field


TOKEN_TYPE_BEARER = "bearer"

class Token(BaseModel):

    access_token: str = Field(description="The access token")
    expires_in: int = Field(default=3600, ge=1, description="The expiration time of the access token in minutes. Must be at least 1 minute.")
    token_type: str = Field(default="bearer", description="The type of the token (default: 'bearer')")
    

    class Config:
        # Enforces that string fields must have at least 1 character if they are provided
        min_anystr_length = 1
        # Strips whitespace from string fields
        anystr_strip_whitespace = True