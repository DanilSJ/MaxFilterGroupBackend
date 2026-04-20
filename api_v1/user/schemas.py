from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    max_id: Optional[int] = None
    email: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class RegisterSchema(BaseModel):
    email: str
    password: str

    model_config = ConfigDict(from_attributes=True)

class RegisterMaxSchema(BaseModel):
    max_id: int

    model_config = ConfigDict(from_attributes=True)


class LoginSchema(BaseModel):
    email: str
    password: str

    model_config = ConfigDict(from_attributes=True)
