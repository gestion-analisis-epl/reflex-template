import psycopg2
from models.users import User

class UsersRepository:
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        
    def obtener_conexion(self):
        return psycopg2.connect(self.database_url)
    
    def cargar_usuarios(self) -> list[dict]:
        query = """
        SELECT username, password, role FROM users
        """
        with self.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                columnas = [col[0] for col in cursor.description]
                return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]

    def obtener_usuario_por_username(self, username: str) -> dict | None:
        query = """
        SELECT username, role
        FROM users
        WHERE username = %s
        """
        with self.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (username,))
                fila = cursor.fetchone()
                if not fila:
                    return None

                columnas = [col[0] for col in cursor.description]
                return dict(zip(columnas, fila))

    def validar_credenciales(self, username: str, password: str) -> dict | None:
        # `password` se compara con `crypt` porque en BD esta hasheada con pgcrypto.
        query = """
        SELECT username, role
        FROM users
        WHERE username = %s
          AND password = crypt(%s, password)
        """
        with self.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (username, password))
                fila = cursor.fetchone()
                if not fila:
                    return None

                columnas = [col[0] for col in cursor.description]
                return dict(zip(columnas, fila))
        