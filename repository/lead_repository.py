import psycopg2
from models.lead import Lead

class LeadRepository:

    def __init__(self, database_url: str):
        self.database_url = database_url

    def obtener_conexion(self):
        return psycopg2.connect(self.database_url)

    # ── Clientes ─────────────────────────────────────────────────────────────

    def cargar_clientes(self) -> list[dict]:
        """Carga id y nombre completo de todos los clientes activos."""
        query = """
        SELECT id_cliente, nombre_cliente || ' ' || apellido_cliente AS nombre_cliente
        FROM todos_clientes
        WHERE nombre_cliente != 'SIN NOMBRE' 
        AND APELLIDO_CLIENTE != 'SIN APELLIDO'
        AND cliente_activo = true
        ORDER BY nombre_cliente
        """
        with self.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                columnas = [col[0] for col in cursor.description]
                return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]

    # ── Ejecutivos ────────────────────────────────────────────────────────────

    def cargar_ejecutivos(self) -> list[dict]:
        """Carga id y nombre de todos los ejecutivos."""
        query = """
        SELECT id_ejecutivo, nombre_completo_ejecutivo AS nombre_ejecutivo
        FROM ejecutivos
        ORDER BY nombre_ejecutivo
        """
        with self.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                columnas = [col[0] for col in cursor.description]
                return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
            
    # ── Seguimientos ────────────────────────────────────────────────────────────    
    def cargar_seguimientos(self)  -> list[dict]:
        query = """
        SELECT id_seguimiento, id_lead, id_ejecutivo, fecha_seguimiento, tipo_seguimiento, notas, proximo_seguimiento, fecha_creacion 
        FROM seguimientos
        ORDER BY fecha_seguimiento
        """
        with self.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                columnas = [col[0] for col in cursor.description]
                return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
    
    def obtener_seguimientos_por_lead(self, id_lead: str) -> list[dict]:
        """Obtiene todos los seguimientos de un lead específico con información del ejecutivo."""
        query = """
        SELECT s.id_seguimiento, s.id_lead, s.id_ejecutivo, s.fecha_seguimiento, 
               s.tipo_seguimiento, s.notas, s.proximo_seguimiento, s.fecha_creacion,
               e.nombre_completo_ejecutivo AS nombre_ejecutivo
        FROM seguimientos s
        LEFT JOIN ejecutivos e ON s.id_ejecutivo = e.id_ejecutivo
        WHERE s.id_lead = %s
        ORDER BY s.fecha_creacion DESC
        """
        with self.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (id_lead,))
                columnas = [col[0] for col in cursor.description]
                return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
    
    def insertar_seguimiento(self, datos: dict) -> str:
        """Inserta un nuevo seguimiento."""
        query = """
        INSERT INTO seguimientos(
            id_lead, id_ejecutivo, fecha_seguimiento, tipo_seguimiento, 
            notas, proximo_seguimiento, fecha_creacion
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id_seguimiento
        """
        with self.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (
                    datos["id_lead"],
                    datos["id_ejecutivo"],
                    datos["fecha_seguimiento"],
                    datos["tipo_seguimiento"],
                    datos["notas"],
                    datos.get("proximo_seguimiento"),
                    datos["fecha_creacion"],
                ))
                conn.commit()
                return cursor.fetchone()[0]
            
    # ── Leads ─────────────────────────────────────────────────────────────────

    def insertar_lead(self, datos: dict) -> str:
        query = """
        INSERT INTO leads(
            id_cliente, id_ejecutivo, fecha_contacto, tipo_origen,
            ciudad_interes, status_actual, monto_cotizacion_mxn,
            fecha_creacion, fecha_ultima_modificacion, fecha_estimada_cierre,
            linea_negocio, servicio_producto_interes, id_interno
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id_lead
        """
        with self.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (
                    datos["id_cliente"],
                    datos["id_ejecutivo"],
                    datos["fecha_contacto"],
                    datos["tipo_origen"],
                    datos["ciudad_interes"],
                    datos["status_actual"],
                    datos["monto_cotizacion_mxn"],
                    datos["fecha_creacion"],
                    datos["fecha_ultima_modificacion"],
                    datos["fecha_estimada_cierre"],
                    datos.get("linea_negocio", []),
                    datos["servicio_producto_interes"],
                    datos["id_interno"],
                ))
                conn.commit()
                return cursor.fetchone()[0]

    def cargar_leads(self) -> list[dict]:
        query = "SELECT * FROM v_leads_detalle"
        with self.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                columnas = [col[0] for col in cursor.description]
                return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]

    def obtener_lead_por_id(self, id_lead: str) -> dict:
        """Obtiene un lead específico por su ID."""
        query = "SELECT * FROM v_leads_detalle WHERE id_lead = %s"
        with self.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (id_lead,))
                columnas = [col[0] for col in cursor.description]
                fila = cursor.fetchone()
                return dict(zip(columnas, fila)) if fila else {}

    def actualizar_lead(self, id_lead: str, datos: dict):
        """Actualiza un lead existente."""
        query = """
        UPDATE leads
        SET id_cliente = %s,
            id_ejecutivo = %s,
            fecha_contacto = %s,
            tipo_origen = %s,
            ciudad_interes = %s,
            status_actual = %s,
            monto_cotizacion_mxn = %s,
            fecha_ultima_modificacion = %s,
            fecha_estimada_cierre = %s,
            linea_negocio = %s,
            servicio_producto_interes = %s,
            id_interno = %s
        WHERE id_lead = %s
        """
        with self.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (
                    datos["id_cliente"],
                    datos["id_ejecutivo"],
                    datos["fecha_contacto"],
                    datos["tipo_origen"],
                    datos["ciudad_interes"],
                    datos["status_actual"],
                    datos["monto_cotizacion_mxn"],
                    datos["fecha_ultima_modificacion"],
                    datos["fecha_estimada_cierre"],
                    datos.get("linea_negocio", []),
                    datos["servicio_producto_interes"],
                    datos["id_interno"],
                    id_lead,
                ))
                conn.commit()

    def eliminar_lead(self, id_lead: str):
        """Elimina un lead por su ID."""
        query = "DELETE FROM leads WHERE id_lead = %s"
        with self.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (id_lead,))
                conn.commit()