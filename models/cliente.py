import reflex as rx
import re
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, field_validator

class Cliente(BaseModel):
    id_cliente: Optional[str] = Field(default=None, primary_key=True)
    nombre_cliente: str = Field(min_length=3, default="")
    apellido_cliente: str = Field(min_length=3, default="")
    empresa_cliente: str = Field(min_length=3, default="")
    telefono_cliente: str = ""
    email_cliente: EmailStr = ""
    estado_origen: str = ""
    tipo_cliente: str = ""
    fecha_registro: Optional[datetime] = None
    ultima_actualizacion: Optional[datetime] = None
    activo: bool = True
    
    @property
    def nombre_completo(self):
        return f'{self.nombre_cliente} {self.apellido_cliente}'
    
    # Limpieza de los strings (strip automátrico)
    @field_validator("*", mode="before")
    @classmethod
    def limpiar_strings(cls, valor):
        if isinstance(valor, str):
            return valor.strip()
        return valor
    
    # Validar que nombre, apellido y empresa no sean solo espacios
    @field_validator("nombre_cliente", "apellido_cliente", "empresa_cliente", "estado_origen")
    @classmethod
    def no_espacios(cls, valor: str):
        if not valor:
            raise ValueError("El campo no puede estar vacío o contener solo espacios")
        return valor
    
    # Normalizar campos en mayúsculas
    @field_validator("nombre_cliente", "apellido_cliente", "empresa_cliente", "estado_origen")
    @classmethod
    def normalizar_campos(cls, valor: str):
        return valor.upper()
    
    # Limpiar número de teléfono
    @field_validator("telefono_cliente")
    @classmethod
    def limpiar_telefono(cls, valor: str):
        if not valor:
            return ""
        telefono_limpio = re.sub(r"\D", "", valor)
        if telefono_limpio and len(telefono_limpio) < 10:
            return telefono_limpio  # Permitir teléfonos cortos de datos existentes
        return telefono_limpio