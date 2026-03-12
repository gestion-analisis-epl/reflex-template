from models.cliente import Cliente
from repository.cliente_repository import ClienteRepository

class ClienteService:
    def __init__(self, repo: ClienteRepository):
        self.repository = repo
        
    def listar_todos(self) -> list[Cliente]:
        todos = self.repository.cargar_clientes()
        clientes = [Cliente(**fila) for fila in todos]
        return clientes
    
    def listar_clientes_activos(self) -> list[Cliente]:
        clientes = self.listar_todos()
        return [c for c in clientes if c.activo]
    
    def crear_cliente(self, cliente: Cliente) -> str:
        return self.repository.insertar_cliente(cliente.model_dump())
    
    def actualizar_cliente(self, id_cliente: str, cliente: Cliente) -> bool:
        return self.repository.actualizar_cliente(id_cliente, cliente.model_dump())
    
    def eliminar_cliente(self, id_cliente: str) -> bool:
        return self.repository.eliminar_cliente(id_cliente)