import pandas as pd
import sqlite3

class DataIO:
    """
    Clase responsable de gestionar la Entrada y Salida (E/S) de datos.
    Aísla la lógica de lectura y escritura de archivos y bases de datos.
    """
    
    @staticmethod
    def cargar_csv(ruta):
        """
        Lee un archivo CSV desde una ruta local.
        Utiliza el motor de python para inferir automáticamente el separador (, o ;).
        
        Args:
            ruta (str): Ruta absoluta o relativa al archivo CSV.
        Returns:
            pd.DataFrame: DataFrame con los datos cargados.
        """
        return pd.read_csv(ruta, sep=None, engine='python')

    @staticmethod
    def cargar_excel(ruta):
        """
        Lee un archivo Excel (.xlsx o .xls).
        
        Args:
            ruta (str): Ruta al archivo Excel.
        Returns:
            pd.DataFrame: DataFrame con los datos de la primera hoja.
        """
        return pd.read_excel(ruta)

    @staticmethod
    def obtener_tablas_sqlite(ruta):
        """
        Consulta el esquema interno de SQLite para obtener los nombres de todas las tablas.
        
        Args:
            ruta (str): Ruta a la base de datos .sqlite o .db.
        Returns:
            list: Lista de strings con los nombres de las tablas disponibles.
        """
        conexion = sqlite3.connect(ruta)
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        tablas = pd.read_sql(query, conexion)['name'].tolist()
        conexion.close()
        return tablas

    @staticmethod
    def cargar_sqlite(ruta, tabla):
        """
        Extrae todos los registros de una tabla específica en una base de datos SQLite.
        
        Args:
            ruta (str): Ruta a la base de datos.
            tabla (str): Nombre de la tabla a consultar.
        Returns:
            pd.DataFrame: DataFrame con los datos de la tabla.
        """
        conexion = sqlite3.connect(ruta)
        df = pd.read_sql(f"SELECT * FROM {tabla}", conexion)
        conexion.close()
        return df

    @staticmethod
    def exportar_csv(df, ruta):
        """
        Guarda un DataFrame en formato CSV sin incluir el índice numérico de Pandas.
        """
        df.to_csv(ruta, index=False)

    @staticmethod
    def exportar_excel(df, ruta):
        """
        Guarda un DataFrame en formato Excel sin incluir el índice numérico.
        """
        df.to_excel(ruta, index=False)