from repository.lead_repository import LeadRepository
from models.lead import Lead
from models.seguimiento import Seguimiento
from datetime import datetime

class LeadService:
    def __init__(self, repo: LeadRepository):
        self.repo = repo

    def obtener_clientes(self) -> list[dict]:
        """Retorna [{"id": ..., "nombre": ...}] de clientes activos."""
        resultados = self.repo.cargar_clientes()
        return [{"id": r["id_cliente"], "nombre": r["nombre_cliente"]} for r in resultados]

    def obtener_ejecutivos(self) -> list[dict]:
        """Retorna [{"id": ..., "nombre": ...}] de ejecutivos."""
        resultados = self.repo.cargar_ejecutivos()
        return [{"id": r["id_ejecutivo"], "nombre": r["nombre_ejecutivo"]} for r in resultados]
    
    def obtener_seguimientos(self) -> list[dict]:
        resultados = self.repo.cargar_seguimientos()
        return [{"id": r["id_seguimiento"], "lead": r["id_lead"]} for r in resultados]

    def insertar_lead(self, datos: dict) -> str:
        """Valida con el modelo Lead e inserta en la BD."""
        ahora = datetime.now()
        datos["fecha_creacion"] = ahora
        datos["fecha_ultima_modificacion"] = ahora

        lead = Lead(**datos)
        return self.repo.insertar_lead(lead.model_dump(exclude={"id_lead"}))

    def cargar_leads(self) -> list[dict]:
        leads = self.repo.cargar_leads()
        
        # Convertir monto_cotizacion_mxn a float y formatearlo como moneda
        for lead in leads:
            if "monto_cotizacion_mxn" in lead:
                monto = float(lead["monto_cotizacion_mxn"]) if lead["monto_cotizacion_mxn"] else 0.0
                lead["monto_cotizacion_mxn"] = monto
                lead["monto_formateado"] = f"${monto:,.2f}"
        return leads

    def obtener_lead_por_id(self, id_lead: str) -> dict:
        """Obtiene un lead por su ID."""
        lead = self.repo.obtener_lead_por_id(id_lead)
        if lead and "monto_cotizacion_mxn" in lead:
            monto = float(lead["monto_cotizacion_mxn"]) if lead["monto_cotizacion_mxn"] else 0.0
            lead["monto_cotizacion_mxn"] = monto
            lead["monto_formateado"] = f"${monto:,.2f}"
        return lead

    def actualizar_lead(self, id_lead: str, datos: dict):
        """Actualiza un lead existente."""
        datos["fecha_ultima_modificacion"] = datetime.now()
        lead = Lead(**datos)
        self.repo.actualizar_lead(id_lead, lead.model_dump(exclude={"id_lead", "fecha_creacion"}))

    def eliminar_lead(self, id_lead: str):
        """Elimina un lead por su ID."""
        self.repo.eliminar_lead(id_lead)
    
    # ── Seguimientos ────────────────────────────────────────────────────────
    
    def obtener_seguimientos_por_lead(self, id_lead: str) -> list[dict]:
        """Obtiene todos los seguimientos de un lead."""
        return self.repo.obtener_seguimientos_por_lead(id_lead)
    
    def insertar_seguimiento(self, datos: dict) -> str:
        """Valida e inserta un nuevo seguimiento."""
        datos["fecha_creacion"] = datetime.now()
        seguimiento = Seguimiento(**datos)
        return self.repo.insertar_seguimiento(seguimiento.model_dump(exclude={"id_seguimiento"}))