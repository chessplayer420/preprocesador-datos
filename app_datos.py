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
            else:
                print("    [✓] 2.2 Manejo de datos faltantes (completado)")
                print("    [-] 2.3 Transformación de datos categóricos (pendiente)")
                
            print("    [X] 2.4 Normalización y escalado (requiere transformación categórica)")
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
            self.seleccion_columnas_lista = True
            self.valores_faltantes_listos = False # Se reinicia si se cambian las columnas

            print(f"Selección guardada: Features = {self.features}, Target = '{self.target}'")

        except (ValueError, IndexError):
            print("⚠ Error: Debe seleccionar al menos una feature y un único target que no esté en las features.")

    def manejar_valores_faltantes(self):
        print("\n==============================")
        print("Manejo de Valores Faltantes")
        print("==============================")
        
        # Criterio: Solo analizar las columnas seleccionadas (features + target)
        columnas_seleccionadas = self.features + [self.target]
        faltantes_por_columna = self.df[columnas_seleccionadas].isnull().sum()
        columnas_con_nulos = faltantes_por_columna[faltantes_por_columna > 0]
        
        # Caso 2: No hay valores faltantes
        if columnas_con_nulos.empty:
            print("No se han detectado valores faltantes en las columnas seleccionadas.")
            print("No es necesario aplicar ninguna estrategia.")
            self.valores_faltantes_listos = True
            return
            
        # Caso 1 y 3: Hay valores faltantes
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
                # Intenta convertir a número si aplica
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
            elif opcion in ['2.3', '2.4', '2.5', '3', '4'] or (opcion == '2' and self.valores_faltantes_listos):
                print(f"\n[!] Esa opción aún está pendiente de implementación o requiere pasos previos.")
            elif opcion == '5':
                break
            else:
                print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    app = DataPipelineLoader()
    app.ejecutar()