import reflex as rx
from models.lead import Lead
from services.lead_service import LeadService
from repository.lead_repository import LeadRepository
from datetime import datetime
import math
from utils.config import DATABASE_URL

class LeadState(rx.State):
    leads: list[dict] = []
    cargando: bool = False
    error: str = ""

    # Formulario
    id_cliente: str = ""
    nombre_cliente: str = ""
    id_ejecutivo: str = ""
    nombre_ejecutivo: str = ""
    fecha_contacto: str = datetime.now().strftime("%Y-%m-%d")
    tipo_origen: str = ""
    ciudad_interes: str = ""
    status_actual: str = ""
    monto_cotizacion_mxn: float = 0.0
    fecha_estimada_cierre: str = datetime.now().strftime("%Y-%m-%d")
    linea_negocio: list[str] = []
    servicio_producto_interes: str = ""
    id_interno: str = ""

    # Opciones para selects
    clientes: list[dict] = []
    ejecutivos: list[dict] = []

    # Estado para editar lead
    lead_seleccionado_id: str = ""
    editando: bool = False

    # Dialog states
    mostrar_dialog_editar: bool = False
    mostrar_dialog_eliminar: bool = False
    mostrar_dialog_ver: bool = False
    lead_id_a_eliminar: str = ""

    # Seguimientos
    seguimientos: list[dict] = []
    lead_actual_detalle: dict = {}

    # Formulario de seguimiento
    tipo_seguimiento: str = ""
    notas_seguimiento: str = ""
    fecha_seguimiento: str = datetime.now().strftime("%Y-%m-%d")
    proximo_seguimiento: str = ""
    id_ejecutivo_seguimiento: str = ""
    nombre_ejecutivo_seguimiento: str = ""

    # Filtros y sort
    filtro_texto: str = ""
    filtro_status: str = ""
    filtro_origen: str = ""
    filtro_ejecutivo: str = ""
    sort_col: str = ""
    sort_asc: bool = True

    # Paginación — guardadas como str para evitar que Reflex las confunda con eventos
    _pagina_actual: str = "1"
    _items_por_pagina: str = "20"

    def _service(self) -> LeadService:
        return LeadService(LeadRepository(DATABASE_URL))

    def cargar_opciones(self):
        self.clientes = self._service().obtener_clientes()
        self.ejecutivos = self._service().obtener_ejecutivos()

    def cargar_leads(self):
        self.cargando = True
        try:
            self.leads = self._service().cargar_leads()
            self._pagina_actual = "1"
        except Exception as e:
            self.error = str(e)
        finally:
            self.cargando = False

    # ── Setters de formulario ────────────────────────────────────────────────

    def set_nombre_cliente(self, nombre: str):
        self.nombre_cliente = nombre
        match = next((c for c in self.clientes if c["nombre"] == nombre), None)
        self.id_cliente = match["id"] if match else ""

    def set_nombre_ejecutivo(self, nombre: str):
        self.nombre_ejecutivo = nombre
        match = next((e for e in self.ejecutivos if e["nombre"] == nombre), None)
        self.id_ejecutivo = match["id"] if match else ""

    def set_nombre_ejecutivo_seguimiento(self, nombre: str):
        self.nombre_ejecutivo_seguimiento = nombre
        match = next((e for e in self.ejecutivos if e["nombre"] == nombre), None)
        self.id_ejecutivo_seguimiento = match["id"] if match else ""

    def set_tipo_seguimiento(self, valor: str):
        self.tipo_seguimiento = valor

    def set_notas_seguimiento(self, valor: str):
        self.notas_seguimiento = valor

    def set_fecha_seguimiento(self, valor: str):
        self.fecha_seguimiento = valor

    def set_proximo_seguimiento(self, valor: str):
        self.proximo_seguimiento = valor

    def set_fecha_contacto(self, valor: str):
        self.fecha_contacto = valor

    def set_tipo_origen(self, valor: str):
        self.tipo_origen = valor

    def set_ciudad_interes(self, valor: str):
        self.ciudad_interes = valor

    def set_status_actual(self, valor: str):
        self.status_actual = valor

    def set_monto(self, valor: str):
        self.monto_cotizacion_mxn = float(valor) if valor else 0.0

    def set_fecha_cierre(self, valor: str):
        self.fecha_estimada_cierre = valor

    def set_id_interno(self, valor: str):
        self.id_interno = valor

    def set_servicio_producto_interes(self, valor: str):
        self.servicio_producto_interes = valor

    def toggle_linea_negocio(self, linea: str, checked: bool):
        if checked and linea not in self.linea_negocio:
            self.linea_negocio = self.linea_negocio + [linea]
        elif not checked and linea in self.linea_negocio:
            self.linea_negocio = [l for l in self.linea_negocio if l != linea]

    # ── CRUD ────────────────────────────────────────────────────────────────

    def crear_lead(self):
        self.cargando = True
        try:
            lead = Lead(
                id_cliente=self.id_cliente,
                id_ejecutivo=self.id_ejecutivo,
                fecha_contacto=datetime.strptime(self.fecha_contacto, "%Y-%m-%d") if self.fecha_contacto else datetime.now(),
                tipo_origen=self.tipo_origen,
                ciudad_interes=self.ciudad_interes,
                status_actual=self.status_actual,
                monto_cotizacion_mxn=float(self.monto_cotizacion_mxn or 0),
                fecha_estimada_cierre=datetime.strptime(self.fecha_estimada_cierre, "%Y-%m-%d") if self.fecha_estimada_cierre else None,
                linea_negocio=self.linea_negocio,
                fecha_creacion=datetime.now(),
                fecha_ultima_modificacion=datetime.now(),
                servicio_producto_interes=self.servicio_producto_interes,
                id_interno=self.id_interno,
            )
            self._service().insertar_lead(lead.model_dump(exclude={"id_lead"}))
            self.limpiar_formulario()
            self.cargar_leads()
        except ValueError as e:
            self.error = str(e)
        finally:
            self.cargando = False

    def limpiar_formulario(self):
        self.lead_seleccionado_id = ""
        self.id_cliente = ""
        self.nombre_cliente = ""
        self.id_ejecutivo = ""
        self.nombre_ejecutivo = ""
        self.fecha_contacto = datetime.now().strftime("%Y-%m-%d")
        self.tipo_origen = ""
        self.ciudad_interes = ""
        self.status_actual = ""
        self.monto_cotizacion_mxn = 0.0
        self.fecha_estimada_cierre = datetime.now().strftime("%Y-%m-%d")
        self.linea_negocio = []
        self.id_interno = ""
        self.servicio_producto_interes = ""
        self.editando = False
        self.mostrar_dialog_editar = False
        self.error = ""

    def cargar_datos_lead(self, id_lead: str):
        if not id_lead:
            self.error = "ID de lead no válido"
            return
        self.cargando = True
        try:
            lead = self._service().obtener_lead_por_id(id_lead)
            if lead:
                self.lead_seleccionado_id = id_lead
                self.id_cliente = str(lead.get("id_cliente", ""))
                self.id_ejecutivo = str(lead.get("id_ejecutivo", ""))
                self.fecha_contacto = lead.get("fecha_contacto").strftime("%Y-%m-%d") if lead.get("fecha_contacto") else ""
                self.tipo_origen = lead.get("tipo_origen", "")
                self.ciudad_interes = lead.get("ciudad_interes", "")
                self.status_actual = lead.get("status_actual", "")
                self.monto_cotizacion_mxn = float(lead.get("monto_cotizacion_mxn", 0.0))
                self.fecha_estimada_cierre = lead.get("fecha_estimada_cierre").strftime("%Y-%m-%d") if lead.get("fecha_estimada_cierre") else ""
                self.linea_negocio = lead.get("linea_negocio", []) if isinstance(lead.get("linea_negocio"), list) else []
                self.id_interno = str(lead.get("id_interno", ""))
                self.servicio_producto_interes = str(lead.get("servicio_producto_interes", ""))

                cliente_match = next((c for c in self.clientes if c["id"] == self.id_cliente), None)
                self.nombre_cliente = cliente_match["nombre"] if cliente_match else ""

                ejecutivo_match = next((e for e in self.ejecutivos if e["id"] == self.id_ejecutivo), None)
                self.nombre_ejecutivo = ejecutivo_match["nombre"] if ejecutivo_match else ""

                self.id_ejecutivo_seguimiento = self.id_ejecutivo
                self.nombre_ejecutivo_seguimiento = self.nombre_ejecutivo

                self.editando = True
                self.mostrar_dialog_editar = True
                self.error = ""
        except Exception as e:
            self.error = f"Error al cargar lead: {e}"
        finally:
            self.cargando = False
        return LeadState.cargar_opciones

    def actualizar_lead(self):
        self.cargando = True
        try:
            lead = Lead(
                id_lead=self.lead_seleccionado_id,
                id_cliente=self.id_cliente,
                id_ejecutivo=self.id_ejecutivo,
                fecha_contacto=datetime.strptime(self.fecha_contacto, "%Y-%m-%d") if self.fecha_contacto else datetime.now(),
                tipo_origen=self.tipo_origen,
                ciudad_interes=self.ciudad_interes,
                status_actual=self.status_actual,
                monto_cotizacion_mxn=float(self.monto_cotizacion_mxn or 0),
                fecha_estimada_cierre=datetime.strptime(self.fecha_estimada_cierre, "%Y-%m-%d") if self.fecha_estimada_cierre else None,
                linea_negocio=self.linea_negocio,
                fecha_ultima_modificacion=datetime.now(),
                id_interno=self.id_interno,
                servicio_producto_interes=self.servicio_producto_interes,
            )
            self._service().actualizar_lead(self.lead_seleccionado_id, lead.model_dump(exclude={"id_lead", "fecha_creacion"}))
            self.limpiar_formulario()
            self.cargar_leads()
        except ValueError as e:
            self.error = str(e)
        finally:
            self.cargando = False

    def preparar_eliminar(self, id_lead: str):
        self.lead_id_a_eliminar = id_lead
        self.mostrar_dialog_eliminar = True

    def eliminar_lead(self):
        self.cargando = True
        try:
            self._service().eliminar_lead(self.lead_id_a_eliminar)
            self.lead_id_a_eliminar = ""
            self.mostrar_dialog_eliminar = False
            self.cargar_leads()
        except Exception as e:
            self.error = str(e)
        finally:
            self.cargando = False

    def cancelar_eliminar(self):
        self.lead_id_a_eliminar = ""
        self.mostrar_dialog_eliminar = False

    # ── Wrappers UI ─────────────────────────────────────────────────────────

    def abrir_dialog(self):
        self.mostrar_dialog_editar = True
        self.editando = False
        self.error = ""
        return LeadState.cargar_opciones

    def cerrar_dialog(self):
        self.mostrar_dialog_editar = False
        self.limpiar_formulario()

    def abrir_dialog_editar(self, id_lead: str):
        return self.cargar_datos_lead(id_lead)

    def abrir_dialog_eliminar(self, id_lead: str):
        return self.preparar_eliminar(id_lead)

    def cerrar_dialog_eliminar(self):
        return self.cancelar_eliminar()

    def confirmar_eliminacion(self):
        return self.eliminar_lead()

    def guardar_lead(self):
        if self.editando and self.lead_seleccionado_id:
            return self.actualizar_lead()
        else:
            return self.crear_lead()

    # ── Seguimientos ────────────────────────────────────────────────────────

    def abrir_dialog_ver(self, id_lead: str):
        if not id_lead:
            self.error = "ID de lead no válido"
            return
        self.cargando = True
        try:
            self.cargar_opciones()
            self.lead_actual_detalle = self._service().obtener_lead_por_id(id_lead)
            self.seguimientos = self._service().obtener_seguimientos_por_lead(id_lead)
            self.lead_seleccionado_id = id_lead

            if self.lead_actual_detalle.get("id_ejecutivo"):
                self.id_ejecutivo_seguimiento = self.lead_actual_detalle.get("id_ejecutivo", "")
                ejecutivo_match = next((e for e in self.ejecutivos if e["id"] == self.id_ejecutivo_seguimiento), None)
                self.nombre_ejecutivo_seguimiento = ejecutivo_match["nombre"] if ejecutivo_match else ""

            self.mostrar_dialog_ver = True
        except Exception as e:
            self.error = f"Error al cargar detalles: {e}"
        finally:
            self.cargando = False

    def cerrar_dialog_ver(self):
        self.mostrar_dialog_ver = False
        self.lead_actual_detalle = {}
        self.seguimientos = []
        self.limpiar_formulario_seguimiento()

    def limpiar_formulario_seguimiento(self):
        self.tipo_seguimiento = ""
        self.notas_seguimiento = ""
        self.fecha_seguimiento = datetime.now().strftime("%Y-%m-%d")
        self.proximo_seguimiento = ""
        self.id_ejecutivo_seguimiento = ""
        self.nombre_ejecutivo_seguimiento = ""

    def agregar_seguimiento(self):
        self.cargando = True
        self.error = ""
        try:
            if not self.id_ejecutivo_seguimiento:
                self.error = "Debes seleccionar un ejecutivo para el seguimiento"
                return
            datos = {
                "id_lead": self.lead_seleccionado_id,
                "id_ejecutivo": self.id_ejecutivo_seguimiento,
                "fecha_seguimiento": datetime.strptime(self.fecha_seguimiento, "%Y-%m-%d"),
                "tipo_seguimiento": self.tipo_seguimiento,
                "notas": self.notas_seguimiento,
                "proximo_seguimiento": datetime.strptime(self.proximo_seguimiento, "%Y-%m-%d") if self.proximo_seguimiento else None,
            }
            self._service().insertar_seguimiento(datos)
            self.limpiar_formulario_seguimiento()
            self.seguimientos = self._service().obtener_seguimientos_por_lead(self.lead_seleccionado_id)
        except ValueError as e:
            self.error = str(e)
        except Exception as e:
            self.error = f"Error al agregar seguimiento: {e}"
        finally:
            self.cargando = False

    # ── Filtros y sort ──────────────────────────────────────────────────────

    def set_filtro_texto(self, valor: str):
        self.filtro_texto = valor
        self._pagina_actual = "1"

    def set_filtro_status(self, valor: str):
        self.filtro_status = "" if valor == "TODOS" else valor
        self._pagina_actual = "1"

    def set_filtro_origen(self, valor: str):
        self.filtro_origen = "" if valor == "TODOS" else valor
        self._pagina_actual = "1"

    def set_filtro_ejecutivo(self, valor: str):
        self.filtro_ejecutivo = "" if valor == "TODOS" else valor
        self._pagina_actual = "1"

    def set_sort_col(self, col: str):
        if self.sort_col == col:
            self.sort_asc = not self.sort_asc
        else:
            self.sort_col = col
            self.sort_asc = True
        self._pagina_actual = "1"

    def limpiar_filtros(self):
        self.filtro_texto = ""
        self.filtro_status = ""
        self.filtro_origen = ""
        self.filtro_ejecutivo = ""
        self.sort_col = ""
        self.sort_asc = True
        self._pagina_actual = "1"

    # ── Paginación ──────────────────────────────────────────────────────────

    def pagina_anterior(self):
        p = int(self._pagina_actual)
        if p > 1:
            self._pagina_actual = str(p - 1)

    def pagina_siguiente(self):
        p = int(self._pagina_actual)
        if p < self.total_paginas:
            self._pagina_actual = str(p + 1)

    def ir_a_pagina(self, pagina: int):
        self._pagina_actual = str(int(pagina))

    def set_items_por_pagina(self, valor: str):
        self._items_por_pagina = str(int(valor))
        self._pagina_actual = "1"

    # ── Kanban ─────────────────────────────────────────────────────
    vista_kanban: bool = False          # toggle tabla ↔ kanban

    def toggle_vista(self):
        self.vista_kanban = not self.vista_kanban

    def actualizar_status_lead(self, id_lead: str, nuevo_status: str):
        """Actualiza solo el status de un lead en la BD."""
        if not id_lead or not nuevo_status:
            return
        self.cargando = True
        try:
            # Obtener el lead actual
            lead_data = self._service().obtener_lead_por_id(id_lead)
            if lead_data:
                # Actualizar solo el status
                lead_data["status_actual"] = nuevo_status
                lead_data["fecha_ultima_modificacion"] = datetime.now()
                # Crear objeto Lead y actualizar
                lead = Lead(**lead_data)
                self._service().actualizar_lead(id_lead, lead.model_dump(exclude={"id_lead", "fecha_creacion"}))
                # Recargar leads para reflejar cambios
                self.cargar_leads()
        except Exception as e:
            self.error = f"Error al actualizar status: {e}"
        finally:
            self.cargando = False

    def cambiar_status_desde_kanban(self, id_lead: str, nuevo_status: str):
        """Método específico para cambiar status desde el kanban."""
        return self.actualizar_status_lead(id_lead, nuevo_status)

    def leads_por_status(self, status: str) -> list[dict]:
        """Retorna los leads filtrados que tienen el status especificado."""
        return [l for l in self.leads_filtrados if l.get("status_actual") == status]

    @rx.var
    def leads_agrupados_por_status(self) -> dict[str, list]:
        """Agrupa leads_filtrados por status_actual."""
        groups: dict[str, list] = {}
        for lead in self.leads_filtrados:
            key = lead.get("status_actual", "SIN STATUS")
            groups.setdefault(key, []).append(lead)
        return groups

    # ── Computed vars ───────────────────────────────────────────────────────

    @rx.var
    def filtro_status_ui(self) -> str:
        return self.filtro_status if self.filtro_status else "TODOS"

    @rx.var
    def filtro_origen_ui(self) -> str:
        return self.filtro_origen if self.filtro_origen else "TODOS"

    @rx.var
    def filtro_ejecutivo_ui(self) -> str:
        return self.filtro_ejecutivo if self.filtro_ejecutivo else "TODOS"

    @rx.var
    def leads_filtrados(self) -> list[dict]:
        result = self.leads

        if self.filtro_texto:
            texto = self.filtro_texto.lower()
            result = [
                l for l in result
                if texto in (l.get("nombre_cliente") or "").lower()
                or texto in (l.get("apellido_cliente") or "").lower()
                or texto in (l.get("nombre_ejecutivo") or "").lower()
                or texto in (l.get("ciudad_interes") or "").lower()
                or texto in (l.get("id_interno") or "").lower()
                or texto in (l.get("servicio_producto_interes") or "").lower()
            ]

        if self.filtro_status:
            result = [l for l in result if l.get("status_actual") == self.filtro_status]

        if self.filtro_origen:
            result = [l for l in result if l.get("tipo_origen") == self.filtro_origen]

        if self.filtro_ejecutivo:
            result = [l for l in result if l.get("nombre_ejecutivo") == self.filtro_ejecutivo]

        if self.sort_col:
            def sort_key(l):
                val = l.get(self.sort_col)
                if val is None:
                    return (1, 0, "")
                if isinstance(val, (int, float)):
                    return (0, val, "")
                return (0, 0, str(val))

            result = sorted(result, key=sort_key, reverse=not self.sort_asc)

        return result

    @rx.var
    def total_leads_filtrados(self) -> int:
        return len(self.leads_filtrados)

    @rx.var
    def total_paginas(self) -> int:
        total = self.total_leads_filtrados
        if total == 0:
            return 1
        return math.ceil(total / int(self._items_por_pagina))

    @rx.var
    def leads_paginados(self) -> list[dict]:
        pagina = int(self._pagina_actual)
        por_pagina = int(self._items_por_pagina)
        inicio = (pagina - 1) * por_pagina
        fin = inicio + por_pagina
        return self.leads_filtrados[inicio:fin]

    @rx.var
    def rango_info(self) -> str:
        total = self.total_leads_filtrados
        if total == 0:
            return "0 resultados"
        pagina = int(self._pagina_actual)
        por_pagina = int(self._items_por_pagina)
        inicio = (pagina - 1) * por_pagina + 1
        fin = min(pagina * por_pagina, total)
        return f"{inicio}–{fin} de {total}"

    @rx.var
    def pagina_actual_int(self) -> int:
        return int(self._pagina_actual)

    @rx.var
    def items_por_pagina_str(self) -> str:
        return self._items_por_pagina

    @rx.var
    def paginas_visibles(self) -> list[int]:
        total = self.total_paginas
        actual = int(self._pagina_actual)
        if total <= 7:
            return list(range(1, total + 1))
        pages = set([1, total, actual])
        if actual > 1:
            pages.add(actual - 1)
        if actual < total:
            pages.add(actual + 1)
        return sorted([p for p in pages if 1 <= p <= total])

    @rx.var
    def conteo_por_status(self) -> dict[str, int]:
        """Retorna un diccionario con el conteo de leads por status."""
        conteo = {}
        for lead in self.leads_filtrados:
            status = lead.get("status_actual", "SIN STATUS")
            conteo[status] = conteo.get(status, 0) + 1
        return conteo