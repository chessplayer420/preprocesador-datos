import pandas as pd

class DataTransformer:
    """
    Clase que agrupa puros métodos estáticos encargados de la transformación, 
    limpieza y escalado de datos (Data Wrangling / Feature Engineering).
    No interactúa con el usuario, solo procesa DataFrames.
    """
    
    @staticmethod
    def manejar_faltantes(df, columnas, estrategia, valor_constante=None):
        """
        Aplica una estrategia de imputación o eliminación para los valores nulos (NaN).
        
        Args:
            df (pd.DataFrame): DataFrame original.
            columnas (list): Lista de columnas donde se buscarán y tratarán nulos.
            estrategia (str): Número en formato string que indica la estrategia ('1' a '5').
            valor_constante (int/float, opcional): Valor a usar si la estrategia es '5'.
            
        Returns:
            pd.DataFrame: Nuevo DataFrame con los nulos gestionados.
        """
        df_proc = df.copy() # Trabajamos sobre una copia para evitar SettingWithCopyWarning
        
        if estrategia == '1':
            # Elimina cualquier fila que tenga al menos un nulo en las columnas especificadas
            df_proc.dropna(subset=columnas, inplace=True)
        elif estrategia == '2':
            # Imputación por Media (solo para variables numéricas)
            for col in columnas:
                if pd.api.types.is_numeric_dtype(df_proc[col]):
                    df_proc[col] = df_proc[col].fillna(df_proc[col].mean())
        elif estrategia == '3':
            # Imputación por Mediana (robusta ante outliers)
            for col in columnas:
                if pd.api.types.is_numeric_dtype(df_proc[col]):
                    df_proc[col] = df_proc[col].fillna(df_proc[col].median())
        elif estrategia == '4':
            # Imputación por Moda (valor más frecuente)
            for col in columnas:
                df_proc[col] = df_proc[col].fillna(df_proc[col].mode()[0])
        elif estrategia == '5' and valor_constante is not None:
            # Imputación por valor definido por el usuario
            for col in columnas:
                df_proc[col] = df_proc[col].fillna(valor_constante)
                
        return df_proc

    @staticmethod
    def codificar_categoricas(df, features_actuales, col_categoricas, estrategia):
        """
        Convierte variables de texto o categóricas en representaciones numéricas.
        
        Args:
            df (pd.DataFrame): DataFrame original.
            features_actuales (list): Lista de características seleccionadas actualmente.
            col_categoricas (list): Sublista de features que son de tipo texto/categoría.
            estrategia (str): '1' para One-Hot Encoding, '2' para Label Encoding.
            
        Returns:
            tuple: (DataFrame transformado, Lista actualizada de features).
        """
        df_proc = df.copy()
        nuevas_features = list(features_actuales)
        
        if estrategia == '1':
            # One-Hot Encoding: Crea variables binarias independientes para cada categoría
            columnas_originales = df_proc.columns.tolist()
            df_proc = pd.get_dummies(df_proc, columns=col_categoricas, dtype=int)
            
            # Actualizamos la lista de features eliminando las originales y añadiendo las binarias
            nuevas_features = [f for f in nuevas_features if f not in col_categoricas]
            nuevas_columnas_generadas = [c for c in df_proc.columns if c not in columnas_originales]
            nuevas_features.extend(nuevas_columnas_generadas)
            
        elif estrategia == '2':
            # Label Encoding: Asigna un entero incremental a cada categoría única (0, 1, 2...)
            for col in col_categoricas:
                df_proc[col] = df_proc[col].astype('category').cat.codes
                
        return df_proc, nuevas_features

    @staticmethod
    def aplicar_escalado(df, columnas, estrategia):
        """
        Normaliza o estandariza las variables numéricas para que compartan la misma escala.
        """
        df_proc = df.copy()
        if estrategia == '1':
            # Min-Max Scaling: Transforma los valores a un rango de [0, 1]
            for col in columnas:
                col_min, col_max = df_proc[col].min(), df_proc[col].max()
                # La condición evita la división por cero si la columna es una constante
                df_proc[col] = (df_proc[col] - col_min) / (col_max - col_min) if col_max != col_min else 0.0
        elif estrategia == '2':
            # Z-score: Estandariza con media = 0 y desviación típica = 1
            for col in columnas:
                col_mean, col_std = df_proc[col].mean(), df_proc[col].std()
                df_proc[col] = (df_proc[col] - col_mean) / col_std if col_std != 0 else 0.0
        return df_proc

    @staticmethod
    def detectar_atipicos(df, columnas):
        """
        Detecta valores atípicos (outliers) utilizando el método del Rango Intercuartílico (IQR).
        
        Returns:
            dict_atipicos: Diccionario con {columna: cantidad_de_atipicos}
            mascaras_atipicos: Diccionario con {columna: pd.Series(booleana)} donde True = outlier
        """
        dict_atipicos = {}
        mascaras_atipicos = {}
        for col in columnas:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            # Límites teóricos de los bigotes del Boxplot
            limite_inferior = Q1 - 1.5 * IQR
            limite_superior = Q3 + 1.5 * IQR
            
            mascara = (df[col] < limite_inferior) | (df[col] > limite_superior)
            if mascara.sum() > 0:
                dict_atipicos[col] = mascara.sum()
                mascaras_atipicos[col] = mascara
                
        return dict_atipicos, mascaras_atipicos

    @staticmethod
    def resolver_atipicos(df, mascaras_atipicos, estrategia):
        """
        Aplica correcciones sobre las filas identificadas como outliers por sus máscaras booleanas.
        """
        df_proc = df.copy()
        if estrategia == '1':
            # Consolida todas las máscaras en una sola y filtra el DataFrame para eliminar filas
            mascara_total = pd.Series(False, index=df_proc.index)
            for mascara in mascaras_atipicos.values():
                mascara_total = mascara_total | mascara
            df_proc = df_proc[~mascara_total] # ~ invierte el booleano (mantenemos lo que NO es outlier)
        elif estrategia == '2':
            # Sustituye los valores extremos usando el operador .loc de pandas por la mediana
            for col, mascara in mascaras_atipicos.items():
                mediana = df_proc[col].median()
                df_proc.loc[mascara, col] = mediana
        return df_proc