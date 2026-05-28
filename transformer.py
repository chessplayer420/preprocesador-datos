import pandas as pd

class DataTransformer:
    """Responsable de aplicar transformaciones matemáticas y limpieza sobre el DataFrame."""
    @staticmethod
    def manejar_faltantes(df, columnas, estrategia, valor_constante=None):
        df_proc = df.copy()
        if estrategia == '1':
            df_proc.dropna(subset=columnas, inplace=True)
        elif estrategia == '2':
            for col in columnas:
                if pd.api.types.is_numeric_dtype(df_proc[col]):
                    df_proc[col] = df_proc[col].fillna(df_proc[col].mean())
        elif estrategia == '3':
            for col in columnas:
                if pd.api.types.is_numeric_dtype(df_proc[col]):
                    df_proc[col] = df_proc[col].fillna(df_proc[col].median())
        elif estrategia == '4':
            for col in columnas:
                df_proc[col] = df_proc[col].fillna(df_proc[col].mode()[0])
        elif estrategia == '5' and valor_constante is not None:
            for col in columnas:
                df_proc[col] = df_proc[col].fillna(valor_constante)
        return df_proc

    @staticmethod
    def codificar_categoricas(df, features_actuales, col_categoricas, estrategia):
        df_proc = df.copy()
        nuevas_features = list(features_actuales)
        
        if estrategia == '1':
            columnas_originales = df_proc.columns.tolist()
            df_proc = pd.get_dummies(df_proc, columns=col_categoricas, dtype=int)
            nuevas_features = [f for f in nuevas_features if f not in col_categoricas]
            nuevas_columnas_generadas = [c for c in df_proc.columns if c not in columnas_originales]
            nuevas_features.extend(nuevas_columnas_generadas)
        elif estrategia == '2':
            for col in col_categoricas:
                df_proc[col] = df_proc[col].astype('category').cat.codes
                
        return df_proc, nuevas_features

    @staticmethod
    def aplicar_escalado(df, columnas, estrategia):
        df_proc = df.copy()
        if estrategia == '1':
            for col in columnas:
                col_min, col_max = df_proc[col].min(), df_proc[col].max()
                df_proc[col] = (df_proc[col] - col_min) / (col_max - col_min) if col_max != col_min else 0.0
        elif estrategia == '2':
            for col in columnas:
                col_mean, col_std = df_proc[col].mean(), df_proc[col].std()
                df_proc[col] = (df_proc[col] - col_mean) / col_std if col_std != 0 else 0.0
        return df_proc

    @staticmethod
    def detectar_atipicos(df, columnas):
        dict_atipicos = {}
        mascaras_atipicos = {}
        for col in columnas:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            mascara = (df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))
            if mascara.sum() > 0:
                dict_atipicos[col] = mascara.sum()
                mascaras_atipicos[col] = mascara
        return dict_atipicos, mascaras_atipicos

    @staticmethod
    def resolver_atipicos(df, mascaras_atipicos, estrategia):
        df_proc = df.copy()
        if estrategia == '1':
            mascara_total = pd.Series(False, index=df_proc.index)
            for mascara in mascaras_atipicos.values():
                mascara_total = mascara_total | mascara
            df_proc = df_proc[~mascara_total]
        elif estrategia == '2':
            for col, mascara in mascaras_atipicos.items():
                mediana = df_proc[col].median()
                df_proc.loc[mascara, col] = mediana
        return df_proc