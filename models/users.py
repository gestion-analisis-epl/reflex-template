import reflex as rx
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator, SecretStr

class User(BaseModel):
    username: str = Field(max_length=255, unique=True)
    password: SecretStr = Field(min_length=7)
    role: str = Field(default="ventas")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)