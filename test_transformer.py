import unittest
import pandas as pd
import numpy as np
from transformer import DataTransformer

class TestDataTransformer(unittest.TestCase):
    
    def setUp(self):
        """Se ejecuta antes de cada prueba. Prepara un DataFrame "sucio" de juguete."""
        self.df_prueba = pd.DataFrame({
            'edad': [20, 25, np.nan, 30, 120],        # 1 nulo, 1 outlier claro (120)
            'salario': [3000, 3500, 4000, np.nan, 5000], # 1 nulo
            'categoria': ['A', 'B', 'A', np.nan, 'C']    # 1 nulo, datos de texto
        })

    # --- Pruebas de Manejo de Faltantes ---
    def test_faltantes_eliminar_filas(self):
        df_res = DataTransformer.manejar_faltantes(self.df_prueba, ['edad', 'salario'], '1')
        self.assertEqual(len(df_res), 3) # Deberían quedar 3 filas sanas

    def test_faltantes_imputar_media(self):
        df_res = DataTransformer.manejar_faltantes(self.df_prueba, ['edad'], '2')
        self.assertFalse(df_res['edad'].isnull().any())
        # La media de [20, 25, 30, 120] es 48.75
        self.assertEqual(df_res.loc[2, 'edad'], 48.75)

    def test_faltantes_valor_constante(self):
        df_res = DataTransformer.manejar_faltantes(self.df_prueba, ['categoria'], '5', valor_constante='Desconocido')
        self.assertEqual(df_res.loc[3, 'categoria'], 'Desconocido')

    # --- Pruebas de Transformación Categórica ---
    def test_codificar_label_encoding(self):
        # Llenamos el nulo para poder codificar
        df_limpio = DataTransformer.manejar_faltantes(self.df_prueba, ['categoria'], '5', valor_constante='A')
        features = ['edad', 'salario', 'categoria']
        
        df_res, nuevas_features = DataTransformer.codificar_categoricas(df_limpio, features, ['categoria'], '2')
        
        # Verificamos que la columna ahora es numérica
        self.assertTrue(pd.api.types.is_numeric_dtype(df_res['categoria']))
        self.assertEqual(len(nuevas_features), 3)

    def test_codificar_one_hot_encoding(self):
        df_limpio = DataTransformer.manejar_faltantes(self.df_prueba, ['categoria'], '5', valor_constante='A')
        features = ['edad', 'salario', 'categoria']
        
        df_res, nuevas_features = DataTransformer.codificar_categoricas(df_limpio, features, ['categoria'], '1')
        
        # Verificamos que la columna original desapareció y se crearon las binarias
        self.assertNotIn('categoria', df_res.columns)
        self.assertIn('categoria_A', df_res.columns)
        self.assertIn('categoria_B', df_res.columns)

    # --- Pruebas de Normalización ---
    def test_escalado_min_max(self):
        df_limpio = DataTransformer.manejar_faltantes(self.df_prueba, ['salario'], '2')
        df_res = DataTransformer.aplicar_escalado(df_limpio, ['salario'], '1')
        
        # El mínimo debe ser 0.0 y el máximo 1.0
        self.assertEqual(df_res['salario'].min(), 0.0)
        self.assertEqual(df_res['salario'].max(), 1.0)

    # --- Pruebas de Valores Atípicos (Outliers) ---
    def test_detectar_y_resolver_atipicos(self):
        # Limpiamos nulos primero
        df_limpio = DataTransformer.manejar_faltantes(self.df_prueba, ['edad'], '5', valor_constante=28)
        
        # Detección
        dict_atipicos, mascaras = DataTransformer.detectar_atipicos(df_limpio, ['edad'])
        
        # Verificamos que detectó el '120' como outlier
        self.assertIn('edad', dict_atipicos)
        self.assertEqual(dict_atipicos['edad'], 1)
        
        # Resolución (Eliminar fila)
        df_res = DataTransformer.resolver_atipicos(df_limpio, mascaras, '1')
        self.assertEqual(len(df_res), 4) # De 5 filas originales, se eliminó 1 outlier

if __name__ == '__main__':
    unittest.main()