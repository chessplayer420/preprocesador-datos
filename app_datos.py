import pandas as pd
import sqlite3
import os

class DataPipelineLoader:
    def __init__(self):
        self.df = None
        self.nombre_archivo = None
        
        # Nuevas variables para la historia de usuario #4
        self.features = []
        self.target = None
        self.seleccion_columnas_lista = False

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
            print("    [-] 2.2 Manejo de datos faltantes (pendiente)")
            print("    [X] 2.3 Transformación de datos categóricos (pendiente)")
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
        """Reinicia la selección si se carga un nuevo dataset."""
        self.features = []
        self.target = None
        self.seleccion_columnas_lista = False

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
            print() # Salto de línea extra para coincidir con la UI solicitada
            feat_input = input("Ingrese los números de las columnas de entrada (features), separados por comas: ")
            print() 
            target_input = input("Ingrese el número de la columna de salida (target): ")
            print()
            
            if not feat_input.strip() or not target_input.strip():
                raise ValueError()

            # Convertir inputs a índices (restando 1 porque el menú empieza en 1)
            feat_indices = [int(x.strip()) - 1 for x in feat_input.split(',')]
            target_index = int(target_input.strip()) - 1

            # Validar que los índices existan
            if any(i < 0 or i >= len(columnas) for i in feat_indices) or target_index < 0 or target_index >= len(columnas):
                raise IndexError()

            # Validar que el target no esté dentro de las features
            if target_index in feat_indices:
                raise ValueError()

            self.features = [columnas[i] for i in feat_indices]
            self.target = columnas[target_index]
            self.seleccion_columnas_lista = True

            print(f"Selección guardada: Features = {self.features}, Target = '{self.target}'")

        except (ValueError, IndexError):
            print("⚠ Error: Debe seleccionar al menos una feature y un único target que no esté en las features.")

    def ejecutar(self):
        while True:
            opcion = self.mostrar_menu_principal()
            
            if opcion == '1':
                self.menu_carga_datos()
            elif opcion in ['2', '2.1']:
                if self.nombre_archivo is None:
                    print("\n[!] Debe cargar un archivo primero (Opción 1).")
                else:
                    self.seleccionar_columnas()
            elif opcion in ['2.2', '2.3', '2.4', '2.5', '3', '4']:
                print(f"\n[!] La opción {opcion} aún está pendiente de implementación o requiere pasos previos.")
            elif opcion == '5':
                break
            else:
                print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    app = DataPipelineLoader()
    app.ejecutar()