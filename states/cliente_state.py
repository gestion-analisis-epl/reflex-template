import reflex as rx
from models.cliente import Cliente
from services.cliente_service import ClienteService
from repository.cliente_repository import ClienteRepository
from datetime import datetime
import math
from utils.config import DATABASE_URL

class ClienteState(rx.State):
    clientes: list[Cliente] = []
    cargando: bool = False
    error: str = ""

    # Formulario
    nombre: str = ""
    apellido: str = ""
    empresa: str = ""
    telefono: str = ""
    email: str = ""
    estado_origen: str = ""
    tipo: str = ""
    fecha_registro: datetime = datetime.now()
    ultima_actualizacion: datetime = datetime.now()
    activo: bool = True
    
    # Estado para editar cliente
    cliente_seleccionado_id: str = ""
    editando: bool = False
    
    # Dialog states
    mostrar_dialog_editar: bool = False
    mostrar_dialog_eliminar: bool = False
    cliente_id_a_eliminar: str = ""

    # Filtros y sort
    filtro_texto: str = ""
    filtro_tipo: str = ""
    filtro_estado: str = ""
    filtro_activo: str = ""
    sort_col: str = ""
    sort_asc: bool = True

    # Paginación — guardadas como str para evitar que Reflex las confunda con eventos
    _pagina_actual: str = "1"
    _items_por_pagina: str = "20"

    def _service(self) -> ClienteService:
        return ClienteService(ClienteRepository(DATABASE_URL))

    def cargar_clientes(self):
        self.cargando = True
        try:
            self.clientes = self._service().listar_todos()
            self._pagina_actual = "1"
        except Exception as e:
            self.error = str(e)
        finally:
            self.cargando = False

    def crear_cliente(self):
        self.cargando = True
        try:
            cliente = Cliente(
                nombre_cliente=self.nombre,
                apellido_cliente=self.apellido,
                empresa_cliente=self.empresa,
                telefono_cliente=self.telefono,
                email_cliente=self.email,
                estado_origen=self.estado_origen,
                tipo_cliente=self.tipo,
                fecha_registro=datetime.now(),
                ultima_actualizacion=datetime.now(),
            )
            self._service().crear_cliente(cliente)
            self.limpiar_formulario()
            self.cargar_clientes()
        except ValueError as e:
            self.error = str(e)
        finally:
            self.cargando = False

    def limpiar_formulario(self):
        """Limpia el formulario y resetea el estado"""
        self.nombre = ""
        self.apellido = ""
        self.empresa = ""
        self.telefono = ""
        self.email = ""
        self.estado_origen = ""
        self.tipo = ""
        self.activo = True
        self.error = ""
        self.cliente_seleccionado_id = ""
        self.editando = False
        self.mostrar_dialog_editar = False
    
    def cargar_datos_cliente(self, id_cliente: str):
        """Carga los datos del cliente para editar"""
        cliente = next((c for c in self.clientes if c.id_cliente == id_cliente), None)
        if cliente:
            self.cliente_seleccionado_id = id_cliente
            self.nombre = cliente.nombre_cliente
            self.apellido = cliente.apellido_cliente
            self.empresa = cliente.empresa_cliente
            self.telefono = cliente.telefono_cliente
            self.email = cliente.email_cliente
            self.estado_origen = cliente.estado_origen
            self.tipo = cliente.tipo_cliente
            self.activo = cliente.activo
            self.editando = True
            self.mostrar_dialog_editar = True
            self.error = ""
    
    def actualizar_cliente(self):
        """Actualiza el cliente seleccionado"""
        self.cargando = True
        try:
            cliente = Cliente(
                id_cliente=self.cliente_seleccionado_id,
                nombre_cliente=self.nombre,
                apellido_cliente=self.apellido,
                empresa_cliente=self.empresa,
                telefono_cliente=self.telefono,
                email_cliente=self.email,
                estado_origen=self.estado_origen,
                tipo_cliente=self.tipo,
                ultima_actualizacion=datetime.now(),
                activo=self.activo,
            )
            self._service().actualizar_cliente(self.cliente_seleccionado_id, cliente)
            self.limpiar_formulario()
            self.cargar_clientes()
        except ValueError as e:
            self.error = str(e)
        finally:
            self.cargando = False
    
    def preparar_eliminar(self, id_cliente: str):
        """Prepara el cliente para eliminar"""
        self.cliente_id_a_eliminar = id_cliente
        self.mostrar_dialog_eliminar = True
    
    def eliminar_cliente(self):
        """Elimina el cliente seleccionado"""
        self.cargando = True
        try:
            self._service().eliminar_cliente(self.cliente_id_a_eliminar)
            self.cliente_id_a_eliminar = ""
            self.mostrar_dialog_eliminar = False
            self.cargar_clientes()
        except Exception as e:
            self.error = str(e)
        finally:
            self.cargando = False
    
    def cancelar_eliminar(self):
        """Cancela la eliminación del cliente"""
        self.cliente_id_a_eliminar = ""
        self.mostrar_dialog_eliminar = False

    # ── Filtros y sort ──────────────────────────────────────────────────────

    def set_filtro_texto(self, valor: str):
        self.filtro_texto = valor
        self._pagina_actual = "1"

    def set_filtro_tipo(self, valor: str):
        self.filtro_tipo = "" if valor == "TODOS" else valor
        self._pagina_actual = "1"

    def set_filtro_estado(self, valor: str):
        self.filtro_estado = "" if valor == "TODOS" else valor
        self._pagina_actual = "1"

    def set_filtro_activo(self, valor: str):
        self.filtro_activo = "" if valor == "TODOS" else valor
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
        self.filtro_tipo = ""
        self.filtro_estado = ""
        self.filtro_activo = ""
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

    # ── Computed vars ───────────────────────────────────────────────────────

    @rx.var
    def filtro_tipo_ui(self) -> str:
        return self.filtro_tipo if self.filtro_tipo else "TODOS"

    @rx.var
    def filtro_estado_ui(self) -> str:
        return self.filtro_estado if self.filtro_estado else "TODOS"

    @rx.var
    def filtro_activo_ui(self) -> str:
        return self.filtro_activo if self.filtro_activo else "TODOS"

    @rx.var
    def clientes_filtrados(self) -> list[Cliente]:
        result = self.clientes

        if self.filtro_texto:
            texto = self.filtro_texto.lower()
            result = [
                c for c in result
                if texto in (c.nombre_cliente or "").lower()
                or texto in (c.apellido_cliente or "").lower()
                or texto in (c.empresa_cliente or "").lower()
                or texto in (c.telefono_cliente or "").lower()
                or texto in (c.email_cliente or "").lower()
            ]

        if self.filtro_tipo:
            result = [c for c in result if c.tipo_cliente == self.filtro_tipo]

        if self.filtro_estado:
            result = [c for c in result if c.estado_origen == self.filtro_estado]

        if self.filtro_activo:
            activo_bool = self.filtro_activo == "SÍ"
            result = [c for c in result if c.activo == activo_bool]

        if self.sort_col:
            def sort_key(c):
                val = getattr(c, self.sort_col, None)
                if val is None:
                    return (1, 0, "")
                if isinstance(val, (int, float)):
                    return (0, val, "")
                return (0, 0, str(val))

            result = sorted(result, key=sort_key, reverse=not self.sort_asc)

        return result

    @rx.var
    def total_clientes_filtrados(self) -> int:
        return len(self.clientes_filtrados)

    @rx.var
    def total_paginas(self) -> int:
        total = self.total_clientes_filtrados
        if total == 0:
            return 1
        return math.ceil(total / int(self._items_por_pagina))

    @rx.var
    def clientes_paginados(self) -> list[Cliente]:
        pagina = int(self._pagina_actual)
        por_pagina = int(self._items_por_pagina)
        inicio = (pagina - 1) * por_pagina
        fin = inicio + por_pagina
        return self.clientes_filtrados[inicio:fin]

    @rx.var
    def rango_info(self) -> str:
        total = self.total_clientes_filtrados
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