from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class UserForm(BaseModel):
    id: Optional[int] = Field(gt=0)
    
    username: str = Field(max_length=30)
    email: EmailStr
    password: str = Field(min_length=6)
    password2: Optional[str]

class TodoForm(BaseModel):
    id: Optional[int] = Field(gt=0)

    title: str = Field(max_length=40)
    description: str = Field(max_length=10)
    importance: int = Field(gt=0, lt=6)
    complete: Optional[bool]
    user_id: Optional[int] = Field(gt=0)
