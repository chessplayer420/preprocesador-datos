import pandas as pd
import sqlite3

class DataIO:
    """Responsable de leer y escribir datos en disco o bases de datos."""
    @staticmethod
    def cargar_csv(ruta):
        return pd.read_csv(ruta, sep=None, engine='python')

    @staticmethod
    def cargar_excel(ruta):
        return pd.read_excel(ruta)

    @staticmethod
    def obtener_tablas_sqlite(ruta):
        conexion = sqlite3.connect(ruta)
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        tablas = pd.read_sql(query, conexion)['name'].tolist()
        conexion.close()
        return tablas

    @staticmethod
    def cargar_sqlite(ruta, tabla):
        conexion = sqlite3.connect(ruta)
        df = pd.read_sql(f"SELECT * FROM {tabla}", conexion)
        conexion.close()
        return df

    @staticmethod
    def exportar_csv(df, ruta):
        df.to_csv(ruta, index=False)

    @staticmethod
    def exportar_excel(df, ruta):
        df.to_excel(ruta, index=False)