import reflex as rx
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

class Producto(BaseModel):
    nombre_producto: str = Field(min_length=3, default="")
    precio_unitario: Decimal = Field(default="0.00")
    cantidad: int = Field(default=1)
    
    @property
    def total_producto(self) -> Decimal:
        return (self.precio_unitario * Decimal(self.cantidad)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    
    @field_validator("precio_unitario")
    @classmethod
    def precio_positivo(cls, valor: Decimal):
        if valor <= Decimal("0.00"):
            raise ValueError("El precio debe ser mayor a 0")
        return valor
    
    @field_validator("cantidad")
    @classmethod
    def cantidad_positiva(cls, valor: int):
        if valor <= Decimal("0.00"):
            raise ValueError("La cantidad debe ser mayor a 0")
        return valor
    
class Cotizacion(BaseModel):
    id_kronos: str
    id_cliente: str
    nombre_cliente: str = Field(min_length=1)
    empresa_cliente: Optional[str] = Field(default="")
    email_cliente: Optional[str] = Field(default="")
    telefono_cliente: Optional[str] = Field(default="")
    estado_origen: Optional[str] = Field(default="")
    
    id_ejecutivo: str
    nombre_ejecutivo: str = Field(min_length=1)
    email_ejecutivo: Optional[str] = Field(default="")
    telefono_ejecutivo: Optional[str] = Field(default="")
    
    fecha_cotizacion: date = Field(default_factory=date.today)
    fecha_vencimiento: Optional[date] = None
    
    incluir_iva: bool = Field(default=True)
    impuesto: Decimal = Field(default="0.16")
    productos: List[Producto] = Field(default_factory=list)
    
    @property
    def subtotal(self):
        return sum([p.total_producto for p in self.productos])
    
    @property
    def iva(self):
        if not self.incluir_iva:
            return Decimal("0.00")
        return self.subtotal * self.impuesto
    
    @property
    def total_con_impuesto(self):
        return self.subtotal + self.iva