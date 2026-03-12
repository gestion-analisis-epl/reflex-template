import psycopg2
from models.ejecutivo import Ejecutivo

class EjecutivoRepository:
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        
    def obtener_conexion(self):
        return psycopg2.connect(self.database_url)
    
    def insertar_ejecutivo(self, datos: dict) -> str:
        """Agrega un nuevo ejecutivo a la base de datos"""
        query = """
        INSERT INTO ejecutivos(nombre_completo_ejecutivo, email_ejecutivo, telefono_ejecutivo, ejecutivo_activo, fecha_alta)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id_ejecutivo
        """