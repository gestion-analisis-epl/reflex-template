import reflex as rx
import re
from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, field_validator, NonNegativeFloat

class Ventas(BaseModel):
    id: Optional[str] = Field(delfault="", primary_key=True),
    id_cliente: str = Field(default=""),
    id_ejecutivo: str = Field(default=""),
    monto_venta_mxn: NonNegativeFloat = Field(default=0)
    fecha_venta: date = Field(default=None)
    folio: Optional[str] = Field(default="")