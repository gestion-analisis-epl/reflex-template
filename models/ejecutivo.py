import reflex as rx
import re
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, field_validator

class Ejecutivo(BaseModel):
    id_ejecutivo: Optional[str] = Field(default=None, primary_key=True)
    nombre_completo_ejecutivo: str = Field(min_length=3, default="")
    email_ejecutivo: EmailStr = ""
    telefono_ejecutivo: str = ""
    ejecutivo_activo: bool = True
    fecha_alta: Optional[datetime] = None
    
    @field_validator("*", mode="before")
    @classmethod
    def limpiar_strings(cls, valor):
        if isinstance(valor, str):
            return valor.strip()
        return valor
    
    @field_validator("nombre_completo_ejecutivo", "email_ejecutivo", "telefono_ejecutivo")
    @classmethod
    def no_espacios(cls, valor: str):
        if not valor:
            raise ValueError("El campo no puede estar vacío o contener solo espacios")
        return valor
    
    # Normalizar campos en mayúsculas
    @field_validator("nombre_completo_ejecutivo")
    @classmethod
    def normalizar_campos(cls, valor: str):
        return valor.upper()
    
    @field_validator("telefono_ejecutivo")
    @classmethod
    def limpiar_telefono(cls, valor: str):
        if not valor:
            return ""
        telefono_limpio = re.sub(r"\D", "", valor)
        if telefono_limpio and len(telefono_limpio) < 10:
            return telefono_limpio  # Permitir teléfonos cortos de datos existentes
        return telefono_limpio