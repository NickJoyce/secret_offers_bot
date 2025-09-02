from pydantic import BaseModel, EmailStr


class Config(BaseModel):
    name: str
    avatar: str | None
    company_logo_url: str | None
    roles: list[str]


class UserCreate(BaseModel):
    """ Validate request data """
    email: EmailStr
    password: str
    config: Config


class UserOutput(BaseModel):
    """ Validate request data """
    id: int
    email: EmailStr
    config: Config
    is_active: bool