import psycopg2

class DashboardRepository:

    def __init__(self, database_url: str):
        self.database_url = database_url

    def obtener_conexion(self):
        return psycopg2.connect(self.database_url)

    def cargar_informacion(self) -> list[dict]:
        """Carga información de la vista detalle de leads"""
        query = """
        SELECT * FROM v_leads_detalle
        ORDER BY nombre_cliente
        """
        with self.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                columnas = [col[0] for col in cursor.description]
                return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]