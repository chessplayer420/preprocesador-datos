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

    def mostrar_menu_principal(self):
        print("\n==============================")
        print("Menú Principal")
        print("==============================")
        
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
            print("[-] 2. Preprocesado de datos")
            print("    [✓] 2.1 Selección de columnas (completado)")
            
            if not self.valores_faltantes_listos:
                print("    [-] 2.2 Manejo de datos faltantes (pendiente)")
                print("    [X] 2.3 Transformación de datos categóricos (requiere manejo de valores faltantes)")
                print("    [X] 2.4 Normalización y escalado (requiere transformación categórica)")
            elif not self.transformacion_categorica_lista:
                print("    [✓] 2.2 Manejo de datos faltantes (completado)")
                print("    [-] 2.3 Transformación de datos categóricos (pendiente)")
                print("    [X] 2.4 Normalización y escalado (requiere transformación categórica)")
            else:
                print("    [✓] 2.2 Manejo de datos faltantes (completado)")
                print("    [✓] 2.3 Transformación de datos categóricos (completado)")
                print("    [-] 2.4 Normalización y escalado (pendiente)")
                
            print("    [X] 2.5 Detección y manejo de valores atípicos (requiere normalización)")
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
        """Reinicia todo el estado del pipeline si se carga un nuevo dataset."""
        self.features = []
        self.target = None
        self.seleccion_columnas_lista = False
        self.valores_faltantes_listos = False
        self.transformacion_categorica_lista = False

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
        
        # Criterio: Solo detectar columnas categóricas dentro de las variables de entrada (features)
        columnas_categoricas = self.df[self.features].select_dtypes(include=['object', 'category']).columns.tolist()
        
        # Caso 2: No hay columnas categóricas
        if not columnas_categoricas:
            print("No se han detectado columnas categóricas en las variables de entrada seleccionadas.")
            print("No es necesario aplicar ninguna transformación.")
            self.transformacion_categorica_lista = True
            return
            
        # Caso 1: Hay columnas categóricas
        print("Se han detectado columnas categóricas en las variables de entrada seleccionadas:")
        for col in columnas_categoricas:
            print(f"  - {col}")
            
        print("\nSeleccione una estrategia de transformación:")
        print("  [1] One-Hot Encoding (genera nuevas columnas binarias)")
        print("  [2] Label Encoding (convierte categorías a números enteros)")
        print("  [3] Volver al menú principal")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            # Guardamos las columnas antes de la transformación para saber cuáles se generan nuevas
            columnas_originales = self.df.columns.tolist()
            
            # Aplicamos One-Hot Encoding
            self.df = pd.get_dummies(self.df, columns=columnas_categoricas, dtype=int)
            
            # Actualizamos self.features quitando las categóricas antiguas y metiendo las nuevas binarias
            self.features = [f for f in self.features if f not in columnas_categoricas]
            nuevas_columnas = [c for c in self.df.columns if c not in columnas_originales]
            self.features.extend(nuevas_columnas)
            
            print("\nTransformación completada con One-Hot Encoding.")
            self.transformacion_categorica_lista = True
            
        elif opcion == '2':
            # Aplicamos Label Encoding utilizando pandas nativo
            for col in columnas_categoricas:
                self.df[col] = self.df[col].astype('category').cat.codes
                
            print("\nTransformación completada con Label Encoding.")
            self.transformacion_categorica_lista = True
            
        elif opcion == '3':
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
            elif opcion in ['2.4', '2.5', '3', '4'] or (opcion == '2' and self.transformacion_categorica_lista):
                print(f"\n[!] Esa opción aún está pendiente de implementación o requiere pasos previos.")
            elif opcion == '5':
                break
            else:
                print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    app = DataPipelineLoader()
    app.ejecutar()