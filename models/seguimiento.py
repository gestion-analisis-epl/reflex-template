from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class Seguimiento(BaseModel):
    id_seguimiento: Optional[str] = Field(default=None, primary_key=True)
    id_lead: str = Field(default="")
    id_ejecutivo: str = Field(default="")
    fecha_seguimiento: datetime = Field(default_factory=datetime.now)
    tipo_seguimiento: str = Field(default="")
    notas: str = Field(default="")
    proximo_seguimiento: Optional[datetime] = None
    fecha_creacion: Optional[datetime] = None
    
    @field_validator("*", mode="before")
    @classmethod
    def limpiar_strings(cls, valor):
        if isinstance(valor, str):
            return valor.strip()
        return valor
    
    @field_validator("notas")
    @classmethod
    def validar_notas(cls, valor: str):
        if not valor or len(valor) < 5:
            raise ValueError("Las notas deben tener al menos 5 caracteres")
        return valor
    
    @field_validator("notas")
    def normalizar_notas(cls, valor: str):
        return valor.upper()