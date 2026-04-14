import reflex as rx 
from repository.dashboard_repository import DashboardRepository
from datetime import datetime
from utils.config import DATABASE_URL

def formatear_monto_compacto(valor: float) -> str:
    """Formatea un monto a formato compacto (10k, 1.5M)"""
    if valor >= 1_000_000:
        return f"${valor/1_000_000:.1f}M"
    elif valor >= 1_000:
        return f"${valor/1_000:.0f}k"
    else:
        return f"${valor:.0f}"

class DashboardState(rx.State):
    # Datos
    leads: list[dict] = []
    is_loading: bool = False
    error_message: str = ""
    
    # Filtros
    filtro_estado_origen: str = "todos"
    filtro_tipo_cliente: str = "todos"
    filtro_linea_negocio: str = "todos"
    filtro_ciudad: str = "todos"
    filtro_status: str = "todos"
    filtro_busqueda: str = ""
    filtro_fecha_inicio: str = ""
    filtro_fecha_fin: str = ""
    
    # UI
    lead_seleccionado_id: str = ""
    
    def cargar_leads(self):
        """Carga los leads desde la base de datos"""
        self.is_loading = True
        self.error_message = ""
        
        try:
            repo = DashboardRepository(DATABASE_URL)
            self.leads = repo.cargar_informacion()
            print(f"Leads cargados: {len(self.leads)}")
        except Exception as e:
            self.error_message = f"Error al cargar datos: {str(e)}"
            print(self.error_message)
        finally:
            self.is_loading = False
    
    # Métodos de filtros
    def cambiar_filtro_estado_origen(self, estado: str):
        self.filtro_estado_origen = estado
    
    def cambiar_filtro_tipo_cliente(self, tipo: str):
        self.filtro_tipo_cliente = tipo
    
    def cambiar_filtro_linea_negocio(self, linea: str):
        self.filtro_linea_negocio = linea
    
    def cambiar_filtro_ciudad(self, ciudad: str):
        self.filtro_ciudad = ciudad

    def cambiar_filtro_status(self, status: str):
        self.filtro_status = status
    
    def cambiar_busqueda(self, valor: str):
        self.filtro_busqueda = valor.lower()
    
    def limpiar_filtros(self):
        """Limpia todos los filtros"""
        self.filtro_estado_origen = "todos"
        self.filtro_tipo_cliente = "todos"
        self.filtro_linea_negocio = "todos"
        self.filtro_ciudad = "todos"
        self.filtro_status = "todos"
        self.filtro_busqueda = ""
        self.filtro_fecha_inicio = ""
        self.filtro_fecha_fin = ""
    
    # COMPUTED VARS - Opciones únicas para filtros
    @rx.var
    def estados_origen_unicos(self) -> list[str]:
        """Retorna lista de estados de origen únicos"""
        estados = set()
        for lead in self.leads:
            estado = lead.get("estado_origen")
            if estado:
                estados.add(str(estado))
        return ["todos"] + sorted(list(estados))
    
    @rx.var
    def tipos_cliente_unicos(self) -> list[str]:
        """Retorna lista de tipos de cliente únicos"""
        tipos = set()
        for lead in self.leads:
            tipo = lead.get("tipo_cliente")
            if tipo:
                tipos.add(str(tipo))
        return ["todos"] + sorted(list(tipos))
    
    @rx.var
    def lineas_negocio_unicas(self) -> list[str]:
        """Retorna lista de líneas de negocio únicas - maneja arrays"""
        lineas = set()
        for lead in self.leads:
            linea = lead.get("linea_negocio")
            if linea:
                # Si es una lista/array, agregar cada elemento
                if isinstance(linea, list):
                    for item in linea:
                        if item:
                            lineas.add(str(item))
                else:
                    # Si es string simple
                    lineas.add(str(linea))
        return ["todos"] + sorted(list(lineas))
    
    @rx.var
    def ciudades_unicas(self) -> list[str]:
        """Retorna lista de ciudades únicas"""
        ciudades = set()
        for lead in self.leads:
            ciudad = lead.get("ciudad_interes")
            if ciudad:
                ciudades.add(str(ciudad))
        return ["todos"] + sorted(list(ciudades))

    @rx.var
    def status_unicos(self) -> list[str]:
        """Retorna lista de status únicos"""
        statuses = set()
        for lead in self.leads:
            status = lead.get("status_actual")
            if status:
                statuses.add(str(status))
        return ["todos"] + sorted(list(statuses))
    
    @rx.var
    def leads_filtrados(self) -> list[dict]:
        """Retorna leads filtrados según los criterios"""
        resultado = self.leads
        
        # Filtro por estado origen
        if self.filtro_estado_origen != "todos":
            resultado = [lead for lead in resultado if str(lead.get("estado_origen")) == self.filtro_estado_origen]
        
        # Filtro por tipo de cliente
        if self.filtro_tipo_cliente != "todos":
            resultado = [lead for lead in resultado if str(lead.get("tipo_cliente")) == self.filtro_tipo_cliente]
        
        # Filtro por línea de negocio - maneja arrays
        if self.filtro_linea_negocio != "todos":
            filtrados = []
            for lead in resultado:
                linea = lead.get("linea_negocio")
                if isinstance(linea, list):
                    # Si es array, verificar si el filtro está en la lista
                    if self.filtro_linea_negocio in [str(item) for item in linea]:
                        filtrados.append(lead)
                else:
                    # Si es string simple
                    if str(linea) == self.filtro_linea_negocio:
                        filtrados.append(lead)
            resultado = filtrados
        
        # Filtro por ciudad
        if self.filtro_ciudad != "todos":
            resultado = [lead for lead in resultado if str(lead.get("ciudad_interes")) == self.filtro_ciudad]

        # Filtro por status de proyecto
        if self.filtro_status != "todos":
            resultado = [lead for lead in resultado if str(lead.get("status_actual")) == self.filtro_status]
        
        # Filtro por búsqueda (nombre, apellido, empresa)
        if self.filtro_busqueda:
            resultado = [
                lead for lead in resultado 
                if self.filtro_busqueda in str(lead.get("nombre_cliente", "")).lower() or
                   self.filtro_busqueda in str(lead.get("apellido_cliente", "")).lower() or
                   self.filtro_busqueda in str(lead.get("empresa_cliente", "")).lower()
            ]
        
        return resultado
    
    # MÉTRICAS PRINCIPALES
    @rx.var
    def total_leads(self) -> int:
        """Total de leads filtrados"""
        return len(self.leads_filtrados)
    
    @rx.var
    def total_leads_sin_filtro(self) -> int:
        """Total de leads sin filtros"""
        return len(self.leads)
    
    @rx.var
    def monto_total_cotizaciones(self) -> float:
        """Suma total de cotizaciones"""
        total = 0.0
        for lead in self.leads_filtrados:
            monto = lead.get("monto_cotizacion_mxn", 0)
            if monto:
                try:
                    total += float(monto)
                except (ValueError, TypeError):
                    pass
        return round(total, 2)

    @rx.var
    def monto_total_cotizaciones_formateado(self) -> str:
        total_float = self.monto_total_cotizaciones
        return str(f"{total_float:,.2f}")
    
    @rx.var
    def monto_promedio_cotizacion(self) -> float:
        """Promedio de cotizaciones"""
        if not self.leads_filtrados:
            return 0.0
        return round(self.monto_total_cotizaciones / len(self.leads_filtrados), 2)

    @rx.var
    def monto_promedio_cotizacion_formateado(self) -> str:
        promedio = self.monto_promedio_cotizacion
        return str(f"{promedio:,.2f}")
    
    @rx.var
    def leads_por_estado_origen(self) -> list[dict]:
        """Cuenta leads por estado de origen para gráficos"""
        conteo = {}
        for lead in self.leads_filtrados:
            estado = str(lead.get("estado_origen", "Sin estado"))
            conteo[estado] = conteo.get(estado, 0) + 1
        return [{"estado": k, "cantidad": v} for k, v in sorted(conteo.items())]

    @rx.var
    def total_por_estado_origen(self) -> list[dict]:
        resumen = {}
        for lead in self.leads_filtrados:
            estado = str(lead.get("estado_origen", "Sin estado"))
            monto = lead.get("monto_cotizacion_mxn", 0)
            try:
                monto_float = float(monto) if monto else 0.0
            except (ValueError, TypeError):
                monto_float = 0.0

            if estado not in resumen:
                resumen[estado] = {"estado": estado, "cantidad": 0, "total": 0.0}
            resumen[estado]["cantidad"] += 1
            resumen[estado]["total"] += monto_float

        resultado = sorted(resumen.values(), key=lambda x: x["total"], reverse=True)
        resultado =[item for item in resultado if item["total"] > 0]    
        
        # Agregar campo formateado
        for item in resultado:
            item["total_fmt"] = formatear_monto_compacto(item["total"])
        
        return resultado
    
    @rx.var
    def leads_por_linea_negocio(self) -> list[dict]:
        """Cuenta leads por línea de negocio - maneja arrays"""
        conteo = {}
        for lead in self.leads_filtrados:
            linea = lead.get("linea_negocio")
            if isinstance(linea, list):
                # Si es array, contar cada línea
                for item in linea:
                    if item:
                        linea_str = str(item)
                        conteo[linea_str] = conteo.get(linea_str, 0) + 1
            else:
                # Si es string simple
                linea_str = str(linea) if linea else "Sin línea"
                conteo[linea_str] = conteo.get(linea_str, 0) + 1
        return [{"linea": k, "cantidad": v} for k, v in sorted(conteo.items())]
    
    @rx.var
    def total_por_linea_negocio(self) -> list[dict]:
        """Monto total por línea de negocio"""
        conteo = {}
        for lead in self.leads_filtrados:
            linea = str(lead.get("linea_negocio", "Sin línea")).strip("[]'\"")
            try:
                monto = float(lead.get("monto_cotizacion_mxn", 0) or 0)
            except (ValueError, TypeError):
                monto = 0.0
                
            if linea in conteo:
                conteo[linea] += monto
            else:
                conteo[linea] = monto
                
        resultado = [
            {
                "linea": k,
                "monto": round(v, 2),
                "monto_fmt": formatear_monto_compacto(v)
            }
            for k, v in sorted(conteo.items(), key=lambda x: x[1], reverse=True) if v > 0
        ]
        return resultado
    
    @rx.var
    def cotizaciones_por_ejecutivo(self) -> list[dict]:
        """Monto de cotizaciones por ejecutivo"""
        conteo = {}
        for lead in self.leads_filtrados:
            ejecutivo = str(lead.get("nombre_ejecutivo", "Sin asignar"))
            try:
                monto = float(lead.get("monto_cotizacion_mxn", 0) or 0)
            except (ValueError, TypeError):
                monto = 0.0
            
            if ejecutivo in conteo:
                conteo[ejecutivo] += monto
            else:
                conteo[ejecutivo] = monto
        
        resultado = [
            {
                "ejecutivo": k, 
                "monto": round(v, 2),
                "monto_fmt": formatear_monto_compacto(v)
            } 
            for k, v in sorted(conteo.items(), key=lambda x: x[1], reverse=True) if v > 0
        ]
        return resultado
    
    @rx.var
    def leads_por_ciudad(self) -> list[dict]:
        """Top 10 ciudades con más leads"""
        conteo = {}
        for lead in self.leads_filtrados:
            ciudad = str(lead.get("ciudad_interes", "Sin ciudad"))
            conteo[ciudad] = conteo.get(ciudad, 0) + 1
        ordenado = sorted(conteo.items(), key=lambda x: x[1], reverse=True)[:10]
        return [{"ciudad": k, "cantidad": v} for k, v in ordenado]
    
    @rx.var
    def leads_por_tipo_cliente(self) -> list[dict]:
        """Distribución por tipo de cliente"""
        conteo = {}
        for lead in self.leads_filtrados:
            tipo = str(lead.get("tipo_cliente", "Sin tipo"))
            conteo[tipo] = conteo.get(tipo, 0) + 1
        return [{"tipo": k, "cantidad": v} for k, v in sorted(conteo.items())]

    @rx.var
    def leads_por_status(self) -> list[dict]:
        fill = ["#8ba7f5", "#bea5f7", "#f7b4bc", "#b5e5f8", "#f3cfc3"]
        conteo = {}
        for lead in self.leads_filtrados:
            status = lead.get("status_actual")
            if isinstance(status, list):
                for item in status:
                    if item:
                        status_str = str(item)
                        conteo[status_str] = conteo.get(status_str, 0) + 1
            else:
                status_str = str(status) if status else "Sin status"
                conteo[status_str] = conteo.get(status_str, 0) + 1
        return [{"status": k, "cantidad": v, "fill": fill[i % len(fill)]} for i, (k, v) in enumerate(sorted(conteo.items(), key=lambda x: x[1], reverse=True))]
    
    @rx.var
    def monto_cotizacion_por_tipo(self) -> list[dict]:
        """Top de cotizaciones por tipo de cliente"""
        resumen = {}
        for lead in self.leads_filtrados:
            tipo = str(lead.get("tipo_cliente", "Sin tipo"))
            monto = lead.get("monto_cotizacion_mxn", 0)
            try:
                monto_float = float(monto) if monto else 0.0
            except (ValueError, TypeError):
                monto_float = 0.0
                
            if tipo not in resumen:
                resumen[tipo] = {"tipo": tipo, "cantidad": 0, "total": 0.0}
            resumen[tipo]["cantidad"] += 1
            resumen[tipo]["total"] += monto_float
            
        resultado = sorted(resumen.values(), key=lambda x: x["total"], reverse=True)
        resultado = [item for item in resultado if item["total"] > 0]
        
        # Agregar campo formateado
        for item in resultado:
            item["total_fmt"] = formatear_monto_compacto(item["total"])
        
        return resultado