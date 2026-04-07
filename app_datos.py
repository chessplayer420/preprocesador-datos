import pandas as pd
import sqlite3
import os

class DataPipelineLoader:
    def __init__(self):
        self.df = None
        self.nombre_archivo = None
        self.preprocesado_listo = False # Para futuros pasos del pipeline

    def mostrar_menu_principal(self):
        print("\n==============================")
        print("Menú Principal")
        print("==============================")
        
        if self.nombre_archivo is None:
            print("[-] 1. Cargar datos (ningún archivo cargado)")
            print("[X] 2. Preprocesado de datos (requiere carga de datos)")
            print("[X] 3. Visualización de datos (requiere carga y preprocesado)")
            print("[X] 4. Exportar datos (requiere carga y preprocesado)")
        else:
            print(f"[✓] 1. Cargar datos (archivo: {self.nombre_archivo})")
            print("[-] 2. Preprocesado de datos (selección de columnas requerida)")
            print("[X] 3. Visualización de datos (requiere preprocesado)")
            print("[X] 4. Exportar datos (requiere preprocesado)")
            
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
            self.mostrar_info_basica()
        except Exception as e:
            print(f"Error al cargar el archivo CSV: {e}")

    def cargar_excel(self):
        ruta = input("Ingrese la ruta del archivo Excel: ")
        try:
            # Si se necesita especificar hoja, se podría añadir lógica aquí, 
            # por ahora carga la primera hoja por defecto para simplificar el flujo
            self.df = pd.read_excel(ruta)
            self.nombre_archivo = os.path.basename(ruta)
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
            conexion.close()
            
            print(f'Datos de la tabla "{tabla_seleccionada}" cargados correctamente.')
            self.mostrar_info_basica(mostrar_mensaje_carga=False)
            
        except Exception as e:
            print(f"Error al cargar la base de datos SQLite: {e}")

    def mostrar_info_basica(self, mostrar_mensaje_carga=True):
        if mostrar_mensaje_carga:
            print("Datos cargados correctamente.")
        
        print(f"Número de filas: {self.df.shape[0]}")
        print(f"Número de columnas: {self.df.shape[1]}")
        print("Primeras 5 filas:")
        # Se imprime sin el índice de dataframe si es posible o limitando el output
        print(self.df.head(5).to_string())

    def ejecutar(self):
        while True:
            opcion = self.mostrar_menu_principal()
            
            if opcion == '1':
                self.menu_carga_datos()
            elif opcion in ['2', '3', '4']:
                if self.nombre_archivo is None:
                    print("\n[!] Debe cargar un archivo primero (Opción 1).")
                else:
                    print(f"\n[!] La opción {opcion} está en construcción para futuras etapas del pipeline.")
            elif opcion == '5':
                break
            else:
                print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    app = DataPipelineLoader()
    app.ejecutar()