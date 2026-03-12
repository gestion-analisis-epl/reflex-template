import psycopg2
from typing import Optional

class CotizacionRepository:
    
    def __init__(self, database_url: str):
        self.database_url = database_url
    
    def obtener_conexion(self):
        return psycopg2.connect(self.database_url)
    
    def obtener_clientes(self) -> list[dict]:
        """Obtiene todos los clientes activos"""
        query = """
        SELECT *
        FROM todos_clientes
        WHERE cliente_activo = true
        AND nombre_cliente != 'SIN NOMBRE'
        AND APELLIDO_CLIENTE != 'SIN APELLIDO'
        ORDER BY nombre_cliente
        """
        with self.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                columnas = [col[0] for col in cursor.description]
                return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
    
    def obtener_ejecutivos(self) -> list[dict]:
        """Obtiene todos los ejecutivos activos"""
        query = """
        SELECT id_ejecutivo, nombre_completo_ejecutivo AS nombre_ejecutivo, email_ejecutivo, telefono_ejecutivo
        FROM ejecutivos
        WHERE ejecutivo_activo = true
        ORDER BY nombre_ejecutivo
        """
        with self.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                columnas = [col[0] for col in cursor.description]
                return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
    
    def generar_id_kronos(self) -> str:
        """Genera un nuevo ID KRON basado en timestamp"""
        from datetime import datetime
        
        # Formato: KRON-YYMMDD-HHMM
        ahora = datetime.now()
        timestamp = ahora.strftime("%y%m%d-%H%M")
        id_kronos = f"KRON-{timestamp}"
        
        # Verificar si ya existe (muy raro, pero posible si se crean 2 en el mismo minuto)
        query = """
        SELECT COUNT(*) FROM cotizaciones WHERE id_kronos = %s
        """
        with self.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (id_kronos,))
                existe = cursor.fetchone()[0] > 0
        
        # Si existe, agregar sufijo de segundos
        if existe:
            segundos = ahora.strftime("%S")
            id_kronos = f"KRON-{timestamp}-{segundos}"
        
        return id_kronos
    
    def insertar_cotizacion(self, datos: dict) -> str:
        """Inserta una cotización y retorna el ID generado"""
        query = """
        INSERT INTO cotizaciones(
            id_kronos, id_cliente, nombre_cliente, empresa_cliente, email_cliente, 
            telefono_cliente, estado_origen, id_ejecutivo, nombre_ejecutivo, 
            email_ejecutivo, telefono_ejecutivo, fecha_cotizacion, fecha_vencimiento, 
            incluir_iva, impuesto, productos_json
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb)
        RETURNING id_kronos
        """
        
        print(f"DEBUG Repo: Conectando a BD...")
        
        with self.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                params = (
                    datos["id_kronos"],
                    datos["id_cliente"],
                    datos["nombre_cliente"],
                    datos["empresa_cliente"],
                    datos["email_cliente"],
                    datos["telefono_cliente"],
                    datos["estado_origen"],
                    datos["id_ejecutivo"],
                    datos["nombre_ejecutivo"],
                    datos["email_ejecutivo"],
                    datos["telefono_ejecutivo"],
                    datos["fecha_cotizacion"],
                    datos["fecha_vencimiento"],
                    datos.get("incluir_iva", True),
                    datos["impuesto"],
                    datos["productos_json"]  # Ya es string JSON
                )
                
                print(f"DEBUG Repo: Ejecutando INSERT con params:")
                for i, p in enumerate(params):
                    print(f"  [{i}] {type(p).__name__}: {str(p)[:100]}")
                
                cursor.execute(query, params)
                conn.commit()
                result = cursor.fetchone()[0]
                print(f"DEBUG Repo: INSERT exitoso, ID retornado: {result}")
                return result
    
    def cargar_cotizaciones(self) -> list[dict]:
        """Obtiene todas las cotizaciones"""
        query = """
        SELECT id_kronos, nombre_cliente, empresa_cliente, nombre_ejecutivo,
               fecha_cotizacion, fecha_vencimiento
        FROM cotizaciones
        ORDER BY fecha_cotizacion DESC
        """
        with self.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                columnas = [col[0] for col in cursor.description]
                return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
    
    def obtener_cotizacion_por_id(self, id_kronos: str) -> Optional[dict]:
        """Obtiene una cotización por su ID"""
        query = """
        SELECT *
        FROM cotizaciones
        WHERE id_kronos = %s
        """
        print(f"DEBUG Repo: Buscando cotización {id_kronos}")
        
        with self.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (id_kronos,))
                columnas = [col[0] for col in cursor.description]
                fila = cursor.fetchone()
                
                if fila:
                    result = dict(zip(columnas, fila))
                    print(f"DEBUG Repo: Cotización encontrada con {len(result)} campos")
                    print(f"DEBUG Repo: productos_json type: {type(result.get('productos_json'))}")
                    return result
                else:
                    print(f"DEBUG Repo: Cotización NO encontrada")
                    return None
