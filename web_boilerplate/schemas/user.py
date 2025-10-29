from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str
    age: int = Field(..., gt=0, description="Age must be positive")
    eye_color: str


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    username: str | None = None
    age: int | None = Field(None, gt=0, description="Age must be positive")
    eye_color: str | None = None


class User(UserBase):
    id: int

    class Config:
        from_attributes = True

