import psycopg2
from models.ventas import Ventas

class VentasRepository:
    def __init__(self, database_url: str):
        self.database_url = database_url

    def obtener_conexion(self):
        return psycopg2.connect(self.database_url)

    def cargar_clientes(self) -> list[str]:
        query = """
        SELECT id_cliente, nombre_cliente || ' ' || apellido_cliente AS nombre_cliente
        FROM todos_clientes
        WHERE cliente_activo = true
        ORDER BY nombre_cliente
        """
        with self.obtener_conexion as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                columnas = [col[0] for col in cursor.description]
                return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]

    def cargar_ejecutivos(self) -> list(str):
        query = """
        SELECT id_ejecutivo, nombre_completo_ejecutivo AS nombre_ejecutivo
        FROM ejecutivos
        ORDER BY nombre_ejecutiv
        """
        with self.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                columnas = [col[0] for col in cursor.description]
                return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]

    
    def insertar_venta(self, datos: dict) -> str:
        query = """
        INSERT INTO ventas(
            id_cliente, id_ejecutivo, monto_venta_mxn, fecha_venta, folio
        )
        VALUES(%s, %s, %s, %s, %s)
        RETURNING id
        """

        with self.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query,(
                    datos["id_cliente"],
                    datos["id_ejecutivo"],
                    datos["monto_venta_mxn"],
                    datos["fecha_venta"],
                    datos["folio"]
                ))
                conn.commit()
                return cursor.fetchone()[0]


    def actualizar_venta(self, id: str, datos: dict):
        query = """
        UPDATE ventas
        SET id_cliente = %s,
            id_ejecutivo = %s,
            monto_venta_mxn = %s,
            fecha_venta = %s,
            folio = %s
        WHERE id = %s
        """
        with self.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (
                    datos["id_cliente"],
                    datos["id_ejecutivo"],
                    datos["monto_venta_mxn"],
                    datos["fecha_venta"],
                    datos["folio"]
                ))
                conn.commit()

    def eliminar_venta(self, id: str, datos: dict):
        query = "DELETE FROM ventas WHERE id = %s"
        with self.obtener_conexion() as conn:
             with conn.cursor() as cursor:
                cursor.execute(query, (id,))
                conn.commit()