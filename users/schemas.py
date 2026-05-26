from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class UserResponse(BaseModel):
    id: int
    name: str 
    email: EmailStr

    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"