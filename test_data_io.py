import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import sqlite3
from data_io import DataIO

class TestDataIO(unittest.TestCase):

    @patch('pandas.read_csv')
    def test_cargar_csv_simulado(self, mock_read_csv):
        """Prueba que cargar_csv llama correctamente a Pandas sin leer el disco."""
        # 1. Configurar el "falso" resultado que devolverá Pandas
        df_falso = pd.DataFrame({'id': [1, 2], 'valor': [10, 20]})
        mock_read_csv.return_value = df_falso

        # 2. Ejecutar el método real de nuestro código
        resultado = DataIO.cargar_csv('ruta/inventada/datos.csv')

        # 3. Afinamos las afirmaciones (Assertions)
        # Verificamos que nuestro código invocó a Pandas con los argumentos exactos
        mock_read_csv.assert_called_once_with('ruta/inventada/datos.csv', sep=None, engine='python')
        # Verificamos que el resultado recibido es el que simulamos
        self.assertEqual(len(resultado), 2)
        self.assertEqual(resultado.iloc[0]['valor'], 10)

    @patch('pandas.read_excel')
    def test_cargar_excel_simulado(self, mock_read_excel):
        """Prueba que cargar_excel invoca el método de Pandas simulado."""
        df_falso = pd.DataFrame({'producto': ['A', 'B']})
        mock_read_excel.return_value = df_falso

        resultado = DataIO.cargar_excel('archivo_imaginario.xlsx')

        mock_read_excel.assert_called_once_with('archivo_imaginario.xlsx')
        self.assertEqual(resultado.iloc[1]['producto'], 'B')

    @patch('sqlite3.connect')
    @patch('pandas.read_sql')
    def test_obtener_tablas_sqlite_simulado(self, mock_read_sql, mock_connect):
        """Simula una conexión a base de datos y la lectura del esquema de tablas."""
        # Creamos un mock para la conexión de sqlite
        mock_conexion = MagicMock()
        mock_connect.return_value = mock_conexion
        
        # Simulamos que la consulta SQL de tablas devuelve este DataFrame
        df_tablas_falsas = pd.DataFrame({'name': ['clientes', 'proveedores']})
        mock_read_sql.return_value = df_tablas_falsas

        # Ejecutamos
        resultado = DataIO.obtener_tablas_sqlite('base_falsa.db')

        # Verificaciones de comportamiento
        mock_connect.assert_called_once_with('base_falsa.db')
        mock_conexion.close.assert_called_once() # Garantiza que cerramos la conexión
        self.assertEqual(resultado, ['clientes', 'proveedores'])

    @patch('pandas.DataFrame.to_csv')
    def test_exportar_csv_simulado(self, mock_to_csv):
        """Verifica que la exportación a CSV configura bien los parámetros."""
        df_para_guardar = pd.DataFrame({'x': [1, 2]})
        
        DataIO.exportar_csv(df_para_guardar, 'salida_test.csv')
        
        # Comprobamos que se ejecutó el guardado y que index=False está activo
        mock_to_csv.assert_called_once_with('salida_test.csv', index=False)

if __name__ == '__main__':
    unittest.main()