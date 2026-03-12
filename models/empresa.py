import reflex as rx 
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, field_validator

class Empresa(BaseModel):
    id_empresa: Optional[str] = Field(default=None, primary_key=True)
    nombre_empresa: str = Field(min_length=3, default="")
    telefono_empresa: str = ""
    email_empresa: EmailStr = ""
    estado_origen: str = ""
    tipo_cliente: str = ""
    fecha_registro: Optional[datetime] = None
    ultima_actualizacion: Optional[datetime] = None
    empresa_activa: bool = True
    
    