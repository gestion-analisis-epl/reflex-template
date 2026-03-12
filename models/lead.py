import reflex as rx
import re
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, NonNegativeFloat, field_validator

class Lead(BaseModel):
    id_lead: Optional[str] = Field(default=None, primary_key=True)
    id_cliente: str = Field(default="")
    id_ejecutivo: str = Field(default="")
    fecha_contacto: datetime = Field(default_factory=datetime.now)
    tipo_origen: str = Field(default="")
    ciudad_interes: str = Field(default="")
    status_actual: str = Field(default="")
    monto_cotizacion_mxn: Optional[NonNegativeFloat] = Field(default=0)
    fecha_creacion: Optional[datetime] = None
    fecha_ultima_modificacion: Optional[datetime] = None
    fecha_estimada_cierre: Optional[datetime] = Field(default_factory=datetime.now)
    linea_negocio: list[str] = Field(default_factory=list)
    servicio_producto_interes: Optional[str] = Field(default="")
    id_interno: Optional[str] = Field(default=None)
    
    @field_validator("*", mode="before")
    @classmethod
    def limpiar_strings(cls, valor):
        if isinstance(valor, str):
            return valor.strip()
        return valor
    
    @field_validator("ciudad_interes")
    @classmethod
    def limpiar_ciudad_interes(cls, valor: str):
        if not valor:
            raise ValueError("El campo no puede estar vacío o contener solo espacios")
        return valor
    
    # Normalizar campos en mayúsculas
    @field_validator("ciudad_interes", "servicio_producto_interes")
    @classmethod
    def normalizar_campos(cls, valor: str):
        return valor.upper()
    
    # Asegurar que el monto sea positivo
    @field_validator("monto_cotizacion_mxn")
    @classmethod
    def monto_positivo(cls, valor: float):
        if valor < 0:
            raise ValueError("El monto debe ser positivo")
        return valor