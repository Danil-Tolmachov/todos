from typing import Optional
from pydantic import BaseModel, Field


class UserForm(BaseModel):
    id: Optional[int]
    
    username: str = Field(max_length=30)
    email: str
    password: str

class TodoForm(BaseModel):
    id: Optional[int]

    title: str = Field(max_length=40)
    description: str
    importance: int = Field(gt=0, lt=6)
    user_id: Optional[int]