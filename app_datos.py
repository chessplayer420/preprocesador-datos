import pandas as pd
import sqlite3
import os

class DataPipelineLoader:
    def __init__(self):
        self.df = None
        self.nombre_archivo = None
        
        # Variables de estado del pipeline
        self.features = []
        self.target = None
        self.seleccion_columnas_lista = False
        self.valores_faltantes_listos = False
        self.transformacion_categorica_lista = False
        self.normalizacion_lista = False
        self.atipicos_listos = False

    def mostrar_menu_principal(self):
        print("\n==============================")
        print("Menú Principal")
        print("==============================")
        
        preprocesado_completado = (self.seleccion_columnas_lista and 
                                   self.valores_faltantes_listos and 
                                   self.transformacion_categorica_lista and 
                                   self.normalizacion_lista and 
                                   self.atipicos_listos)
        
        if self.nombre_archivo is None:
            print("[-] 1. Cargar datos (ningún archivo cargado)")
            print("[X] 2. Preprocesado de datos (requiere carga de datos)")
            print("[X] 3. Visualización de datos (requiere carga y preprocesado)")
            print("[X] 4. Exportar datos (requiere carga y preprocesado)")
        elif not self.seleccion_columnas_lista:
            print(f"[✓] 1. Cargar datos (archivo: {self.nombre_archivo})")
            print("[-] 2. Preprocesado de datos (selección de columnas requerida)")
            print("[X] 3. Visualización de datos (requiere preprocesado)")
            print("[X] 4. Exportar datos (requiere preprocesado)")
        else:
            print(f"[✓] 1. Cargar datos (archivo: {self.nombre_archivo})")
            
            if preprocesado_completado:
                print("[✓] 2. Preprocesado de datos")
            else:
                print("[-] 2. Preprocesado de datos")
                
            print("    [✓] 2.1 Selección de columnas (completado)")
            
            if not self.valores_faltantes_listos:
                print("    [-] 2.2 Manejo de datos faltantes (pendiente)")
                print("    [X] 2.3 Transformación de datos categóricos (requiere manejo de valores faltantes)")
                print("    [X] 2.4 Normalización y escalado (requiere transformación categórica)")
                print("    [X] 2.5 Detección y manejo de valores atípicos (requiere normalización)")
            elif not self.transformacion_categorica_lista:
                print("    [✓] 2.2 Manejo de datos faltantes (completado)")
                print("    [-] 2.3 Transformación de datos categóricos (pendiente)")
                print("    [X] 2.4 Normalización y escalado (requiere transformación categórica)")
                print("    [X] 2.5 Detección y manejo de valores atípicos (requiere normalización)")
            elif not self.normalizacion_lista:
                print("    [✓] 2.2 Manejo de datos faltantes (completado)")
                print("    [✓] 2.3 Transformación de datos categóricos (completado)")
                print("    [-] 2.4 Normalización y escalado (pendiente)")
                print("    [X] 2.5 Detección y manejo de valores atípicos (requiere normalización)")
            elif not self.atipicos_listos:
                print("    [✓] 2.2 Manejo de datos faltantes (completado)")
                print("    [✓] 2.3 Transformación de datos categóricos (completado)")
                print("    [✓] 2.4 Normalización y escalado (completado)")
                print("    [-] 2.5 Detección y manejo de valores atípicos (pendiente)")
            else:
                print("    [✓] 2.2 Manejo de datos faltantes (completado)")
                print("    [✓] 2.3 Transformación de datos categóricos (completado)")
                print("    [✓] 2.4 Normalización y escalado (completado)")
                print("    [✓] 2.5 Detección y manejo de valores atípicos (completado)")
                
            if preprocesado_completado:
                print("[-] 3. Visualización de datos (pendiente)")
            else:
                print("[X] 3. Visualización de datos (requiere preprocesado completo)")
                
            print("[X] 4. Exportar datos (requiere preprocesado completo)")
            
        print("[✓] 5. Salir")
        
        return input("Seleccione una opción: ")

    def menu_carga_datos(self):
        while True:
            print("\n==============================")
            print("Carga de Datos")
            print("==============================")
            print("Seleccione el tipo de archivo a cargar:")
            print("  [1] CSV")
            print("  [2] Excel")
            print("  [3] SQLite")
            print("  [4] Volver al menú principal")
            
            opcion = input("Seleccione una opción: ")
            
            if opcion == '1':
                self.cargar_csv()
                if self.df is not None: break
            elif opcion == '2':
                self.cargar_excel()
                if self.df is not None: break
            elif opcion == '3':
                self.cargar_sqlite()
                if self.df is not None: break
            elif opcion == '4':
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    def cargar_csv(self):
        ruta = input("Ingrese la ruta del archivo: ")
        try:
            self.df = pd.read_csv(ruta, sep=None, engine='python')
            self.nombre_archivo = os.path.basename(ruta)
            self.resetear_preprocesado()
            self.mostrar_info_basica()
        except Exception as e:
            print(f"Error al cargar el archivo CSV: {e}")

    def cargar_excel(self):
        ruta = input("Ingrese la ruta del archivo Excel: ")
        try:
            self.df = pd.read_excel(ruta)
            self.nombre_archivo = os.path.basename(ruta)
            self.resetear_preprocesado()
            self.mostrar_info_basica()
        except Exception as e:
            print(f"Error al cargar el archivo Excel: {e}")

    def cargar_sqlite(self):
        ruta = input("Ingrese la ruta de la base de datos SQLite: ")
        try:
            conexion = sqlite3.connect(ruta)
            query_tablas = "SELECT name FROM sqlite_master WHERE type='table';"
            tablas = pd.read_sql(query_tablas, conexion)['name'].tolist()
            
            if not tablas:
                print("La base de datos está vacía.")
                conexion.close()
                return

            print("Tablas disponibles en la base de datos:")
            for i, tabla in enumerate(tablas):
                print(f"  [{i+1}] {tabla}")
                
            opcion_tabla = int(input("Seleccione una tabla: ")) - 1
            tabla_seleccionada = tablas[opcion_tabla]
            
            self.df = pd.read_sql(f"SELECT * FROM {tabla_seleccionada}", conexion)
            self.nombre_archivo = f"{os.path.basename(ruta)} ({tabla_seleccionada})"
            self.resetear_preprocesado()
            conexion.close()
            
            print(f'Datos de la tabla "{tabla_seleccionada}" cargados correctamente.')
            self.mostrar_info_basica(mostrar_mensaje_carga=False)
            
        except Exception as e:
            print(f"Error al cargar la base de datos SQLite: {e}")

    def resetear_preprocesado(self):
        """Reinicia todo el estado del pipeline."""
        self.features = []
        self.target = None
        self.seleccion_columnas_lista = False
        self.valores_faltantes_listos = False
        self.transformacion_categorica_lista = False
        self.normalizacion_lista = False
        self.atipicos_listos = False

    def mostrar_info_basica(self, mostrar_mensaje_carga=True):
        if mostrar_mensaje_carga:
            print("Datos cargados correctamente.")
        print(f"Número de filas: {self.df.shape[0]}")
        print(f"Número de columnas: {self.df.shape[1]}")
        print("Primeras 5 filas:")
        print(self.df.head(5).to_string())

    def seleccionar_columnas(self):
        print("\n==============================")
        print("Selección de Columnas")
        print("==============================")
        print("Columnas disponibles en los datos:")
        
        columnas = self.df.columns.tolist()
        for i, col in enumerate(columnas):
            print(f"  [{i+1}] {col}")
            
        try:
            print() 
            feat_input = input("Ingrese los números de las columnas de entrada (features), separados por comas: ")
            print() 
            target_input = input("Ingrese el número de la columna de salida (target): ")
            print()
            
            if not feat_input.strip() or not target_input.strip():
                raise ValueError()

            feat_indices = [int(x.strip()) - 1 for x in feat_input.split(',')]
            target_index = int(target_input.strip()) - 1

            if any(i < 0 or i >= len(columnas) for i in feat_indices) or target_index < 0 or target_index >= len(columnas):
                raise IndexError()

            if target_index in feat_indices:
                raise ValueError()

            self.features = [columnas[i] for i in feat_indices]
            self.target = columnas[target_index]
            
            # Actualizamos estados
            self.seleccion_columnas_lista = True
            self.valores_faltantes_listos = False
            self.transformacion_categorica_lista = False
            self.normalizacion_lista = False
            self.atipicos_listos = False

            print(f"Selección guardada: Features = {self.features}, Target = '{self.target}'")

        except (ValueError, IndexError):
            print("⚠ Error: Debe seleccionar al menos una feature y un único target que no esté en las features.")

    def manejar_valores_faltantes(self):
        print("\n==============================")
        print("Manejo de Valores Faltantes")
        print("==============================")
        
        columnas_seleccionadas = self.features + [self.target]
        faltantes_por_columna = self.df[columnas_seleccionadas].isnull().sum()
        columnas_con_nulos = faltantes_por_columna[faltantes_por_columna > 0]
        
        if columnas_con_nulos.empty:
            print("No se han detectado valores faltantes en las columnas seleccionadas.")
            print("No es necesario aplicar ninguna estrategia.")
            self.valores_faltantes_listos = True
            return
            
        print("Se han detectado valores faltantes en las siguientes columnas seleccionadas:")
        for col, count in columnas_con_nulos.items():
            print(f"  - {col}: {count} valores faltantes")
            
        print("\nSeleccione una estrategia para manejar los valores faltantes:")
        print("  [1] Eliminar filas con valores faltantes")
        print("  [2] Rellenar con la media de la columna")
        print("  [3] Rellenar con la mediana de la columna")
        print("  [4] Rellenar con la moda de la columna")
        print("  [5] Rellenar con un valor constante")
        print("  [6] Volver al menú principal")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            self.df.dropna(subset=columnas_con_nulos.index, inplace=True)
            print("\nFilas con valores faltantes eliminadas.")
            self.valores_faltantes_listos = True
        elif opcion == '2':
            for col in columnas_con_nulos.index:
                if pd.api.types.is_numeric_dtype(self.df[col]):
                    self.df[col] = self.df[col].fillna(self.df[col].mean())
            print("\nValores faltantes rellenados con la media de cada columna.")
            self.valores_faltantes_listos = True
        elif opcion == '3':
            for col in columnas_con_nulos.index:
                if pd.api.types.is_numeric_dtype(self.df[col]):
                    self.df[col] = self.df[col].fillna(self.df[col].median())
            print("\nValores faltantes rellenados con la mediana de cada columna.")
            self.valores_faltantes_listos = True
        elif opcion == '4':
            for col in columnas_con_nulos.index:
                self.df[col] = self.df[col].fillna(self.df[col].mode()[0])
            print("\nValores faltantes rellenados con la moda de cada columna.")
            self.valores_faltantes_listos = True
        elif opcion == '5':
            valor = input("\nSeleccione un valor numérico para reemplazar los valores faltantes: ")
            try:
                valor_constante = float(valor) if '.' in valor else int(valor)
            except ValueError:
                valor_constante = valor
            for col in columnas_con_nulos.index:
                self.df[col] = self.df[col].fillna(valor_constante)
            print(f"Valores faltantes reemplazados con el valor {valor_constante}.")
            self.valores_faltantes_listos = True
        elif opcion == '6':
            return
        else:
            print("\nOpción no válida. Intente de nuevo.")

    def transformar_datos_categoricos(self):
        print("\n==============================")
        print("Transformación de Datos Categóricos")
        print("==============================")
        
        columnas_categoricas = self.df[self.features].select_dtypes(include=['object', 'category']).columns.tolist()
        
        if not columnas_categoricas:
            print("No se han detectado columnas categóricas en las variables de entrada seleccionadas.")
            print("No es necesario aplicar ninguna transformación.")
            self.transformacion_categorica_lista = True
            return
            
        print("Se han detectado columnas categóricas en las variables de entrada seleccionadas:")
        for col in columnas_categoricas:
            print(f"  - {col}")
            
        print("\nSeleccione una estrategia de transformación:")
        print("  [1] One-Hot Encoding (genera nuevas columnas binarias)")
        print("  [2] Label Encoding (convierte categorías a números enteros)")
        print("  [3] Volver al menú principal")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            columnas_originales = self.df.columns.tolist()
            self.df = pd.get_dummies(self.df, columns=columnas_categoricas, dtype=int)
            self.features = [f for f in self.features if f not in columnas_categoricas]
            nuevas_columnas = [c for c in self.df.columns if c not in columnas_originales]
            self.features.extend(nuevas_columnas)
            print("\nTransformación completada con One-Hot Encoding.")
            self.transformacion_categorica_lista = True
        elif opcion == '2':
            for col in columnas_categoricas:
                self.df[col] = self.df[col].astype('category').cat.codes
            print("\nTransformación completada con Label Encoding.")
            self.transformacion_categorica_lista = True
        elif opcion == '3':
            return
        else:
            print("\nOpción no válida. Intente de nuevo.")

    def normalizar_y_escalar(self):
        print("\n==============================")
        print("Normalización y Escalado")
        print("==============================")
        
        columnas_numericas = self.df[self.features].select_dtypes(include=['number']).columns.tolist()
        
        if not columnas_numericas:
            print("No se han detectado columnas numéricas en las variables de entrada seleccionadas.")
            print("No es necesario aplicar ninguna normalización.")
            self.normalizacion_lista = True
            return
            
        print("Se han detectado columnas numéricas en las variables de entrada seleccionadas:")
        for col in columnas_numericas:
            print(f"  - {col}")
            
        print("\nSeleccione una estrategia de normalización:")
        print("  [1] Min-Max Scaling (escala valores entre 0 y 1)")
        print("  [2] Z-score Normalization (media 0, desviación estándar 1)")
        print("  [3] Volver al menú principal")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            for col in columnas_numericas:
                col_min = self.df[col].min()
                col_max = self.df[col].max()
                if col_max != col_min:
                    self.df[col] = (self.df[col] - col_min) / (col_max - col_min)
                else:
                    self.df[col] = 0.0
            print("\nNormalización completada con Min-Max Scaling.")
            self.normalizacion_lista = True
        elif opcion == '2':
            for col in columnas_numericas:
                col_mean = self.df[col].mean()
                col_std = self.df[col].std()
                if col_std != 0:
                    self.df[col] = (self.df[col] - col_mean) / col_std
                else:
                    self.df[col] = 0.0
            print("\nNormalización completada con Z-score Normalization.")
            self.normalizacion_lista = True
        elif opcion == '3':
            return
        else:
            print("\nOpción no válida. Intente de nuevo.")

    def detectar_y_manejar_atipicos(self):
        print("\n==============================")
        print("Detección y Manejo de Valores Atípicos")
        print("==============================")
        
        columnas_numericas = self.df[self.features].select_dtypes(include=['number']).columns.tolist()
        
        # Diccionarios para almacenar la información de los outliers encontrados
        dict_atipicos = {}
        mascaras_atipicos = {}
        
        # Algoritmo IQR
        for col in columnas_numericas:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            limite_inferior = Q1 - 1.5 * IQR
            limite_superior = Q3 + 1.5 * IQR
            
            mascara = (self.df[col] < limite_inferior) | (self.df[col] > limite_superior)
            cantidad = mascara.sum()
            
            if cantidad > 0:
                dict_atipicos[col] = cantidad
                mascaras_atipicos[col] = mascara
                
        # Caso 2: No se detectan valores atípicos
        if not dict_atipicos:
            print("No se han detectado valores atípicos en las columnas seleccionadas.")
            print("No es necesario aplicar ninguna estrategia.")
            self.atipicos_listos = True
            return
            
        # Caso 1: Sí se detectan
        print("Se han detectado valores atípicos en las siguientes columnas numéricas seleccionadas:")
        for col, cantidad in dict_atipicos.items():
            print(f"  - {col}: {cantidad} valores atípicos detectados")
            
        print("\nSeleccione una estrategia para manejar los valores atípicos:")
        print("  [1] Eliminar filas con valores atípicos")
        print("  [2] Reemplazar valores atípicos con la mediana de la columna")
        print("  [3] Mantener valores atípicos sin cambios")
        print("  [4] Volver al menú principal")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            # Creamos una máscara global combinando todas las máscaras individuales
            mascara_total = pd.Series(False, index=self.df.index)
            for mascara in mascaras_atipicos.values():
                mascara_total = mascara_total | mascara
                
            self.df = self.df[~mascara_total]
            print("\nFilas con valores atípicos eliminadas.")
            self.atipicos_listos = True
            
        elif opcion == '2':
            for col, mascara in mascaras_atipicos.items():
                mediana = self.df[col].median()
                self.df.loc[mascara, col] = mediana
            print("\nValores atípicos reemplazados con la mediana de cada columna.")
            self.atipicos_listos = True
            
        elif opcion == '3':
            print("\nSe han mantenido los valores atípicos sin cambios.")
            self.atipicos_listos = True
            
        elif opcion == '4':
            return
        else:
            print("\nOpción no válida. Intente de nuevo.")

    def ejecutar(self):
        while True:
            opcion = self.mostrar_menu_principal()
            
            if opcion == '1':
                self.menu_carga_datos()
            elif opcion == '2.1' or (opcion == '2' and not self.seleccion_columnas_lista):
                if self.nombre_archivo is None:
                    print("\n[!] Debe cargar un archivo primero (Opción 1).")
                else:
                    self.seleccionar_columnas()
            elif opcion == '2.2' or (opcion == '2' and self.seleccion_columnas_lista and not self.valores_faltantes_listos):
                if not self.seleccion_columnas_lista:
                    print("\n[!] Debe realizar la selección de columnas primero (Opción 2.1).")
                else:
                    self.manejar_valores_faltantes()
            elif opcion == '2.3' or (opcion == '2' and self.valores_faltantes_listos and not self.transformacion_categorica_lista):
                if not self.valores_faltantes_listos:
                    print("\n[!] Debe gestionar los valores faltantes primero (Opción 2.2).")
                else:
                    self.transformar_datos_categoricos()
            elif opcion == '2.4' or (opcion == '2' and self.transformacion_categorica_lista and not self.normalizacion_lista):
                if not self.transformacion_categorica_lista:
                    print("\n[!] Debe transformar los datos categóricos primero (Opción 2.3).")
                else:
                    self.normalizar_y_escalar()
            elif opcion == '2.5' or (opcion == '2' and self.normalizacion_lista and not self.atipicos_listos):
                if not self.normalizacion_lista:
                    print("\n[!] Debe normalizar y escalar los datos primero (Opción 2.4).")
                else:
                    self.detectar_y_manejar_atipicos()
            elif opcion == '3' or (opcion == '2' and self.atipicos_listos):
                if not self.atipicos_listos:
                    print("\n[!] Debe completar todo el preprocesado antes de visualizar los datos.")
                else:
                    print("\n[!] Módulo de Visualización de Datos en construcción...")
            elif opcion == '4':
                print(f"\n[!] La opción 4 aún está pendiente de implementación.")
            elif opcion == '5':
                break
            else:
                print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    app = DataPipelineLoader()
    app.ejecutar()

