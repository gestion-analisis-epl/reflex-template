from repository.ventas_repository import VentasRepository
from models.ventas import Ventas
from datetime import date

class VentasService:
    def __init__(self, repo: VentasRepository):
        self.repo = repo

    def obtener_clientes(self) -> list[dict]:
        """Retorna [{"id": ..., "nombre": ...}] de clientes activos."""
        resultados = self.repo.cargar_clientes()
        return [{"id": r["id_cliente"], "nombre": r["nombre_cliente"]} for r in resultados]

    def obtener_ejecutivos(self) -> list[dict]:
        """Retorna [{"id": ..., "nombre": ...}] de ejecutivos."""
        resultados = self.repo.cargar_ejecutivos()
        return [{"id": r["id_ejecutivo"], "nombre": r["nombre_ejecutivo"]} for r in resultados]