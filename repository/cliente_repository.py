import psycopg2
from models.cliente import Cliente

class ClienteRepository:

    def __init__(self, database_url: str):
        self.database_url = database_url

    def obtener_conexion(self):
        return psycopg2.connect(self.database_url)
    
    def insertar_cliente(self, datos: dict) -> str:
        """Agrega un nuevo cliente a la base de datos"""
        query = """
        INSERT INTO clientes(nombre_cliente, apellido_cliente, empresa_cliente, telefono_cliente, email_cliente, estado_origen,
        tipo_cliente, fecha_registro, ultima_actualizacion, cliente_activo)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id_cliente
        """
        with self.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query,(
                    datos["nombre_cliente"],
                    datos["apellido_cliente"],
                    datos["empresa_cliente"],
                    datos["telefono_cliente"],
                    datos["email_cliente"],
                    datos["estado_origen"],
                    datos["tipo_cliente"],
                    datos["fecha_registro"],
                    datos["ultima_actualizacion"],
                    datos["activo"]
                ))
                conn.commit()
                return cursor.fetchone()[0]

    def cargar_clientes(self) -> list[dict]:
        """
        Carga todos los clientes de la vista todos_clientes

        Returns:
            list[dict]: Lista de clientes en formato diccionario
        """
        query = """
        SELECT * FROM todos_clientes 
        WHERE nombre_cliente != 'SIN NOMBRE' 
        AND APELLIDO_CLIENTE != 'SIN APELLIDO'
        ORDER BY nombre_cliente, apellido_cliente
        """

        with self.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                columnas = [col[0] for col in cursor.description]
                resultados = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
                
                # Mapear cliente_activo a activo para compatibilidad con el modelo
                for cliente in resultados:
                    if 'cliente_activo' in cliente:
                        cliente['activo'] = cliente.pop('cliente_activo')
                    if 'fecha_registro' not in cliente:
                        cliente['fecha_registro'] = None
                    if 'ultima_actualizacion' not in cliente:
                        cliente['ultima_actualizacion'] = None
                
                return resultados
    
    def actualizar_cliente(self, id_cliente: str, datos: dict) -> bool:
        """Actualiza un cliente existente"""
        query = """
        UPDATE clientes 
        SET nombre_cliente = %s, apellido_cliente = %s, empresa_cliente = %s, 
            telefono_cliente = %s, email_cliente = %s, estado_origen = %s,
            tipo_cliente = %s, ultima_actualizacion = %s, cliente_activo = %s
        WHERE id_cliente = %s
        """
        with self.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (
                    datos["nombre_cliente"],
                    datos["apellido_cliente"],
                    datos["empresa_cliente"],
                    datos["telefono_cliente"],
                    datos["email_cliente"],
                    datos["estado_origen"],
                    datos["tipo_cliente"],
                    datos["ultima_actualizacion"],
                    datos["activo"],
                    id_cliente
                ))
                conn.commit()
                return cursor.rowcount > 0
    
    def eliminar_cliente(self, id_cliente: str) -> bool:
        """Elimina un cliente de la base de datos"""
        query = "DELETE FROM clientes WHERE id_cliente = %s"
        with self.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (id_cliente,))
                conn.commit()
                return cursor.rowcount > 0
        