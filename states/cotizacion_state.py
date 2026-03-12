import reflex as rx
from models.cotizacion import Cotizacion, Producto
from services.cotizacion_service import CotizacionService
from repository.cotizacion_repository import CotizacionRepository
from templates.template_cotizacion import generar_pdf_cotizacion
from datetime import date, timedelta
from decimal import Decimal
import os
from utils.config import DATABASE_URL

class CotizacionState(rx.State):
    cotizaciones: list[dict] = []
    cargando: bool = False
    error: str = ""
    
    # Formulario principal
    id_kronos: str = ""
    
    # Cliente
    id_cliente: str = ""
    nombre_cliente: str = ""
    empresa_cliente: str = ""
    email_cliente: str = ""
    telefono_cliente: str = ""
    estado_origen: str = ""
    
    # Ejecutivo
    id_ejecutivo: str = ""
    nombre_ejecutivo: str = ""
    email_ejecutivo: str = ""
    telefono_ejecutivo: str = ""
    
    # Fechas
    fecha_cotizacion: str = date.today().strftime("%Y-%m-%d")
    fecha_vencimiento: str = (date.today() + timedelta(days=30)).strftime("%Y-%m-%d")
    
    # Impuesto
    incluir_iva: bool = True
    impuesto: str = "0.16"  # Decimal interno (0.16 = 16%)
    impuesto_porcentaje: str = "16"  # Para mostrar al usuario
    
    # Productos
    productos: list[dict] = []
    
    # Formulario de producto
    nombre_producto: str = ""
    precio_unitario: str = "0.00"
    cantidad: str = "1"
    
    # Opciones para selects
    clientes: list[dict] = []
    ejecutivos: list[dict] = []
    
    # Dialogs
    mostrar_dialog_nueva: bool = False
    mostrar_dialog_producto: bool = False
    
    def _service(self) -> CotizacionService:
        return CotizacionService(CotizacionRepository(DATABASE_URL))
    
    def cargar_opciones(self):
        """Carga clientes y ejecutivos"""
        self.clientes = self._service().obtener_clientes()
        self.ejecutivos = self._service().obtener_ejecutivos()
    
    def cargar_cotizaciones(self):
        """Carga todas las cotizaciones"""
        self.cargando = True
        try:
            self.cotizaciones = self._service().cargar_cotizaciones()
        except Exception as e:
            self.error = str(e)
        finally:
            self.cargando = False
    
    def set_cliente(self, nombre: str):
        """Auto-completa los datos del cliente seleccionado"""
        self.nombre_cliente = nombre
        cliente = next((c for c in self.clientes if c["nombre"] == nombre), None)
        if cliente:
            self.id_cliente = cliente["id"]
            self.empresa_cliente = cliente["empresa"]
            self.email_cliente = cliente["email"] or ""
            self.telefono_cliente = cliente["telefono"] or ""
            self.estado_origen = cliente["estado"]
    
    def set_ejecutivo(self, nombre: str):
        """Auto-completa los datos del ejecutivo seleccionado"""
        self.nombre_ejecutivo = nombre
        ejecutivo = next((e for e in self.ejecutivos if e["nombre"] == nombre), None)
        if ejecutivo:
            self.id_ejecutivo = ejecutivo["id"]
            self.email_ejecutivo = ejecutivo["email"] or ""
            self.telefono_ejecutivo = ejecutivo["telefono"] or ""
    
    def set_fecha_cotizacion(self, valor: str):
        self.fecha_cotizacion = valor
    
    def set_fecha_vencimiento(self, valor: str):
        self.fecha_vencimiento = valor
    
    def set_incluir_iva(self, valor: bool):
        """Activa/desactiva el IVA"""
        self.incluir_iva = valor
    
    def set_impuesto_porcentaje(self, valor: str):
        """Recibe porcentaje (ej: 16) y lo convierte a decimal (0.16)"""
        try:
            if valor.strip():
                # Convertir de porcentaje a decimal
                porcentaje = float(valor)
                self.impuesto_porcentaje = valor
                self.impuesto = str(porcentaje / 100)
            else:
                self.impuesto_porcentaje = "0"
                self.impuesto = "0.00"
        except ValueError:
            # Si el valor no es numérico, no hacer nada
            pass
    
    # ── Productos ────────────────────────────────────────────────────────
    
    def abrir_dialog_producto(self):
        """Abre el dialog para agregar producto"""
        self.mostrar_dialog_producto = True
        self.error = ""
    
    def cerrar_dialog_producto(self):
        """Cierra el dialog de producto"""
        self.mostrar_dialog_producto = False
        self.nombre_producto = ""
        self.precio_unitario = "0.00"
        self.cantidad = "1"
    
    def agregar_producto(self):
        """Agrega un producto a la lista"""
        try:
            if not self.nombre_producto.strip():
                self.error = "El nombre del producto es requerido"
                return
            
            producto = {
                "nombre_producto": self.nombre_producto,
                "precio_unitario": float(self.precio_unitario),
                "cantidad": int(self.cantidad),
                "total": float(self.precio_unitario) * int(self.cantidad)
            }
            
            self.productos.append(producto)
            self.cerrar_dialog_producto()
            self.error = ""
        except ValueError as e:
            self.error = f"Error en los datos del producto: {e}"
    
    def eliminar_producto(self, index: int):
        """Elimina un producto de la lista"""
        if 0 <= index < len(self.productos):
            self.productos.pop(index)
    
    def calcular_subtotal(self) -> float:
        """Calcula el subtotal de todos los productos"""
        return sum(p["total"] for p in self.productos)
    
    def calcular_iva(self) -> float:
        """Calcula el IVA solo si está activado"""
        if not self.incluir_iva:
            return 0.0
        subtotal = self.calcular_subtotal()
        return subtotal * float(self.impuesto)
    
    def calcular_total(self) -> float:
        """Calcula el total con o sin impuestos según configuración"""
        return self.calcular_subtotal() + self.calcular_iva()
    
    # ── Crear cotización ────────────────────────────────────────────────
    
    def abrir_dialog_nueva(self):
        """Abre el dialog para nueva cotización"""
        self.cargar_opciones()
        self.id_kronos = self._service().generar_nuevo_id()
        self.mostrar_dialog_nueva = True
        self.limpiar_formulario()
    
    def cerrar_dialog_nueva(self):
        """Cierra el dialog de nueva cotización"""
        self.mostrar_dialog_nueva = False
        self.limpiar_formulario()
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.id_cliente = ""
        self.nombre_cliente = ""
        self.empresa_cliente = ""
        self.email_cliente = ""
        self.telefono_cliente = ""
        self.estado_origen = ""
        self.id_ejecutivo = ""
        self.nombre_ejecutivo = ""
        self.email_ejecutivo = ""
        self.telefono_ejecutivo = ""
        self.fecha_cotizacion = date.today().strftime("%Y-%m-%d")
        self.fecha_vencimiento = (date.today() + timedelta(days=30)).strftime("%Y-%m-%d")
        self.incluir_iva = True
        self.impuesto = "0.16"
        self.impuesto_porcentaje = "16"
        self.productos = []
        self.error = ""
    
    def guardar_cotizacion(self):
        """Guarda la cotización en la BD y genera el PDF"""
        self.cargando = True
        self.error = ""
        try:
            # Validaciones
            if not self.id_cliente:
                self.error = "Debes seleccionar un cliente"
                self.cargando = False
                return
            
            if not self.id_ejecutivo:
                self.error = "Debes seleccionar un ejecutivo"
                self.cargando = False
                return
            
            if not self.productos:
                self.error = "Debes agregar al menos un producto"
                self.cargando = False
                return
            
            # Convertir productos a objetos Producto
            productos_obj = [
                Producto(
                    nombre_producto=p["nombre_producto"],
                    precio_unitario=Decimal(str(p["precio_unitario"])),
                    cantidad=p["cantidad"]
                )
                for p in self.productos
            ]
            
            datos = {
                "id_kronos": self.id_kronos,
                "id_cliente": self.id_cliente,
                "nombre_cliente": self.nombre_cliente,
                "empresa_cliente": self.empresa_cliente or "",
                "email_cliente": self.email_cliente or "",
                "telefono_cliente": self.telefono_cliente or "",
                "estado_origen": self.estado_origen or "",
                "id_ejecutivo": self.id_ejecutivo,
                "nombre_ejecutivo": self.nombre_ejecutivo,
                "email_ejecutivo": self.email_ejecutivo or "",
                "telefono_ejecutivo": self.telefono_ejecutivo or "",
                "fecha_cotizacion": date.fromisoformat(self.fecha_cotizacion),
                "fecha_vencimiento": date.fromisoformat(self.fecha_vencimiento) if self.fecha_vencimiento else None,
                "incluir_iva": self.incluir_iva,
                "impuesto": Decimal(self.impuesto),
                "productos": productos_obj
            }
            
            # Guardar en BD
            print(f"DEBUG: Guardando cotización con datos: {datos}")
            id_guardado = self._service().crear_cotizacion(datos)
            print(f"DEBUG: Cotización guardada con ID: {id_guardado}")
            
            # Generar PDF
            self.generar_pdf(id_guardado)
            
            # Recargar lista y cerrar dialog
            self.cargar_cotizaciones()
            self.cerrar_dialog_nueva()
            
        except ValueError as e:
            import traceback
            self.error = f"Error de validación: {str(e)}\n{traceback.format_exc()}"
            print(f"ERROR ValueError: {traceback.format_exc()}")
        except Exception as e:
            import traceback
            self.error = f"Error: {str(e)}\n{traceback.format_exc()}"
            print(f"ERROR Exception: {traceback.format_exc()}")
        finally:
            self.cargando = False
    
    def generar_pdf(self, id_kronos: str):
        """Genera el PDF de la cotización"""
        try:
            print(f"DEBUG State: Generando PDF para {id_kronos}")
            
            # Obtener la cotización
            cotizacion = self._service().obtener_cotizacion_por_id(id_kronos)
            
            print(f"DEBUG State: Cotización obtenida: {cotizacion is not None}")
            
            if not cotizacion:
                self.error = "Cotización no encontrada"
                return
            
            # Crear directorio de documentos si no existe
            docs_dir = os.path.join(os.getcwd(), "documentos", "cotizaciones")
            os.makedirs(docs_dir, exist_ok=True)
            
            print(f"DEBUG State: Directorio creado: {docs_dir}")
            
            # Ruta del PDF
            ruta_pdf = os.path.join(docs_dir, f"{id_kronos}.pdf")
            
            print(f"DEBUG State: Llamando a generar_pdf_cotizacion...")
            
            # Generar PDF
            if generar_pdf_cotizacion(cotizacion, ruta_pdf):
                print(f"DEBUG State: PDF generado exitosamente en {ruta_pdf}")
                
                # Abrir el PDF
                import platform
                import subprocess
                
                if platform.system() == 'Windows':
                    os.startfile(ruta_pdf)
                elif platform.system() == 'Darwin':  # macOS
                    subprocess.call(['open', ruta_pdf])
                else:  # Linux
                    subprocess.call(['xdg-open', ruta_pdf])
                
                self.error = ""
            else:
                self.error = "Error al generar el PDF"
                print(f"DEBUG State: generar_pdf_cotizacion retornó False")
                
        except Exception as e:
            import traceback
            self.error = f"Error al generar PDF: {e}"
            print(f"ERROR generar_pdf: {traceback.format_exc()}")

