from repository.cotizacion_repository import CotizacionRepository
from models.cotizacion import Cotizacion
import json
from decimal import Decimal

class CotizacionService:
    def __init__(self, repo: CotizacionRepository):
        self.repo = repo
    
    def obtener_clientes(self) -> list[dict]:
        """Retorna lista de clientes formateada para selects"""
        clientes = self.repo.obtener_clientes()
        return [{
            "id": str(c["id_cliente"]),
            "nombre": f"{c['nombre_cliente']} {c['apellido_cliente']}",
            "empresa": c["empresa_cliente"] or "",
            "telefono": c["telefono_cliente"] or "",
            "email": c["email_cliente"] or "",
            "estado": c["estado_origen"] or ""
        } for c in clientes]
    
    def obtener_ejecutivos(self) -> list[dict]:
        """Retorna lista de ejecutivos formateada para selects"""
        ejecutivos = self.repo.obtener_ejecutivos()
        return [{
            "id": str(e["id_ejecutivo"]),
            "nombre": e["nombre_ejecutivo"],
            "email": e["email_ejecutivo"] or "",
            "telefono": e["telefono_ejecutivo"] or ""
        } for e in ejecutivos]
    
    def generar_nuevo_id(self) -> str:
        """Genera un nuevo ID KRON"""
        return self.repo.generar_id_kronos()
    
    def crear_cotizacion(self, datos: dict) -> str:
        """Valida y crea una nueva cotización"""
        print(f"DEBUG Service: Recibiendo datos para crear cotización")
        
        # Convertir productos a JSON
        productos_json = json.dumps([p.model_dump() for p in datos["productos"]], default=str)
        datos["productos_json"] = productos_json
        
        print(f"DEBUG Service: productos_json = {productos_json[:100]}...")
        
        # Convertir Decimal a string para JSON
        if isinstance(datos.get("impuesto"), Decimal):
            datos["impuesto"] = str(datos["impuesto"])
        
        # Convertir fechas a string si son objetos date
        if hasattr(datos.get("fecha_cotizacion"), "isoformat"):
            datos["fecha_cotizacion"] = datos["fecha_cotizacion"]
        if hasattr(datos.get("fecha_vencimiento"), "isoformat"):
            datos["fecha_vencimiento"] = datos["fecha_vencimiento"]
        
        print(f"DEBUG Service: Validando con modelo Cotizacion")
        
        # Validar con el modelo
        cotizacion = Cotizacion(**datos)
        
        print(f"DEBUG Service: Validación exitosa, insertando en BD")
        
        # Insertar en BD
        return self.repo.insertar_cotizacion(datos)
    
    def cargar_cotizaciones(self) -> list[dict]:
        """Obtiene todas las cotizaciones"""
        return self.repo.cargar_cotizaciones()
    
    def obtener_cotizacion_por_id(self, id_kronos: str) -> dict:
        """Obtiene una cotización por ID"""
        print(f"DEBUG Service: Obteniendo cotización {id_kronos}")
        
        cotizacion = self.repo.obtener_cotizacion_por_id(id_kronos)
        
        print(f"DEBUG Service: Cotización encontrada: {cotizacion is not None}")
        
        if cotizacion and "productos_json" in cotizacion:
            print(f"DEBUG Service: productos_json type: {type(cotizacion['productos_json'])}")
            
            # PostgreSQL JSONB ya retorna como objeto Python, no necesita json.loads()
            if isinstance(cotizacion["productos_json"], str):
                print(f"DEBUG Service: productos_json es string, parseando...")
                cotizacion["productos"] = json.loads(cotizacion["productos_json"])
            else:
                # Ya es una lista/dict de Python
                print(f"DEBUG Service: productos_json ya es objeto Python")
                cotizacion["productos"] = cotizacion["productos_json"]
        
        return cotizacion
