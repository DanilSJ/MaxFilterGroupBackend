from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    email: str

    model_config = ConfigDict(from_attributes=True)


class RegisterSchema(BaseModel):
    email: str
    password: str

    model_config = ConfigDict(from_attributes=True)


class LoginSchema(BaseModel):
    email: str
    password: str

    model_config = ConfigDict(from_attributes=True)
