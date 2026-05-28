import os
import pandas as pd

# Importamos las clases desde nuestros módulos locales
from data_io import DataIO
from transformer import DataTransformer
from visualizer import DataVisualizer

class PipelineConsoleUI:
    """Gestiona el flujo del usuario, el menú y mantiene el estado general (Contexto)."""
    def __init__(self):
        self.df = None
        self.df_original = None
        self.nombre_archivo = None
        self.features = []
        self.target = None
        
        self.estados = {
            'seleccion_columnas': False,
            'valores_faltantes': False,
            'trans_categorica': False,
            'normalizacion': False,
            'atipicos': False,
            'visualizacion': False,
            'exportacion': False
        }

    def is_preprocesado_ok(self):
        return all([self.estados['seleccion_columnas'], self.estados['valores_faltantes'], 
                    self.estados['trans_categorica'], self.estados['normalizacion'], self.estados['atipicos']])

    def reset_estados(self):
        self.features, self.target, self.df_original = [], None, None
        for key in self.estados:
            self.estados[key] = False

    def mostrar_info_basica(self):
        print("Datos cargados correctamente.")
        print(f"Número de filas: {self.df.shape[0]}\nNúmero de columnas: {self.df.shape[1]}")
        print("Primeras 5 filas:\n", self.df.head(5).to_string())

    def menu_principal(self):
        while True:
            print("\n==============================\nMenú Principal\n==============================")
            p_ok = self.is_preprocesado_ok()
            
            if self.nombre_archivo is None:
                print("[-] 1. Cargar datos (ningún archivo cargado)\n[X] 2. Preprocesado de datos (requiere carga de datos)\n[X] 3. Visualización de datos (requiere carga y preprocesado)\n[X] 4. Exportar datos (requiere carga y preprocesado)\n[✓] 5. Salir")
            elif not self.estados['seleccion_columnas']:
                print(f"[✓] 1. Cargar datos (archivo: {self.nombre_archivo})\n[-] 2. Preprocesado de datos (selección de columnas requerida)\n[X] 3. Visualización de datos (requiere preprocesado)\n[X] 4. Exportar datos (requiere preprocesado)\n[✓] 5. Salir")
            else:
                print(f"[✓] 1. Cargar datos (archivo: {self.nombre_archivo})")
                print(f"[{'✓' if p_ok else '-'}] 2. Preprocesado de datos")
                print("    [✓] 2.1 Selección de columnas (completado)")
                
                if not self.estados['valores_faltantes']:
                    print("    [-] 2.2 Manejo de datos faltantes (pendiente)\n    [X] 2.3 Transformación de datos categóricos\n    [X] 2.4 Normalización y escalado\n    [X] 2.5 Detección y manejo de valores atípicos")
                elif not self.estados['trans_categorica']:
                    print("    [✓] 2.2 Manejo de datos faltantes (completado)\n    [-] 2.3 Transformación de datos categóricos (pendiente)\n    [X] 2.4 Normalización y escalado\n    [X] 2.5 Detección y manejo de valores atípicos")
                elif not self.estados['normalizacion']:
                    print("    [✓] 2.2 Manejo de datos faltantes (completado)\n    [✓] 2.3 Transformación de datos categóricos (completado)\n    [-] 2.4 Normalización y escalado (pendiente)\n    [X] 2.5 Detección y manejo de valores atípicos")
                elif not self.estados['atipicos']:
                    print("    [✓] 2.2 Manejo de datos faltantes (completado)\n    [✓] 2.3 Transformación de datos categóricos (completado)\n    [✓] 2.4 Normalización y escalado (completado)\n    [-] 2.5 Detección y manejo de valores atípicos (pendiente)")
                else:
                    print("    [✓] 2.2 Manejo de datos faltantes (completado)\n    [✓] 2.3 Transformación de datos categóricos (completado)\n    [✓] 2.4 Normalización y escalado (completado)\n    [✓] 2.5 Detección y manejo de valores atípicos (completado)")
                    
                if p_ok:
                    if not self.estados['visualizacion']:
                        print("[-] 3. Visualización de datos (pendiente)\n[X] 4. Exportar datos (requiere visualización)")
                    else:
                        print("[✓] 3. Visualización de datos (completado)")
                        print(f"[{'✓' if self.estados['exportacion'] else '-'}] 4. Exportar datos ({'completado' if self.estados['exportacion'] else 'pendiente'})")
                else:
                    print("[X] 3. Visualización de datos (requiere preprocesado completo)\n[X] 4. Exportar datos (requiere preprocesado completo)")
                print("[✓] 5. Salir")
                
            opcion = input("Seleccione una opción: ")
            self.enrutar_opcion(opcion)

    def enrutar_opcion(self, opcion):
        if opcion == '1': self.ui_cargar_datos()
        elif opcion == '2.1' or (opcion == '2' and not self.estados['seleccion_columnas']):
            self.ui_seleccionar_columnas() if self.nombre_archivo else print("\n[!] Cargue un archivo primero.")
        elif opcion == '2.2' or (opcion == '2' and self.estados['seleccion_columnas'] and not self.estados['valores_faltantes']):
            self.ui_faltantes() if self.estados['seleccion_columnas'] else print("\n[!] Seleccione columnas primero.")
        elif opcion == '2.3' or (opcion == '2' and self.estados['valores_faltantes'] and not self.estados['trans_categorica']):
            self.ui_categoricas() if self.estados['valores_faltantes'] else print("\n[!] Gestione nulos primero.")
        elif opcion == '2.4' or (opcion == '2' and self.estados['trans_categorica'] and not self.estados['normalizacion']):
            self.ui_normalizar() if self.estados['trans_categorica'] else print("\n[!] Transforme categóricas primero.")
        elif opcion == '2.5' or (opcion == '2' and self.estados['normalizacion'] and not self.estados['atipicos']):
            self.ui_atipicos() if self.estados['normalizacion'] else print("\n[!] Normalice primero.")
        elif opcion == '3':
            if not self.is_preprocesado_ok():
                print("\n==============================\nVisualización de Datos\n==============================\nNo es posible visualizar los datos hasta que se complete el preprocesado.\nPor favor, finalice el manejo de valores atípicos antes de continuar.")
            else: self.ui_visualizar()
        elif opcion == '4':
            self.ui_exportar()
        elif opcion == '5':
            print("\n¡Gracias por utilizar el Pipeline de Datos! Hasta la próxima.\n")
            exit()
        else: print("Opción no válida.")

    def ui_cargar_datos(self):
        print("\n==============================\nCarga de Datos\n==============================\nSeleccione el tipo de archivo a cargar:\n  [1] CSV\n  [2] Excel\n  [3] SQLite\n  [4] Volver")
        op = input("Seleccione una opción: ")
        try:
            if op == '1':
                ruta = input("Ingrese la ruta del archivo: ")
                self.df = DataIO.cargar_csv(ruta)
                self.nombre_archivo = os.path.basename(ruta)
            elif op == '2':
                ruta = input("Ingrese la ruta del archivo Excel: ")
                self.df = DataIO.cargar_excel(ruta)
                self.nombre_archivo = os.path.basename(ruta)
            elif op == '3':
                ruta = input("Ingrese la ruta de la base SQLite: ")
                tablas = DataIO.obtener_tablas_sqlite(ruta)
                if not tablas: return print("La BD está vacía.")
                for i, t in enumerate(tablas): print(f"  [{i+1}] {t}")
                t_idx = int(input("Seleccione una tabla: ")) - 1
                self.df = DataIO.cargar_sqlite(ruta, tablas[t_idx])
                self.nombre_archivo = f"{os.path.basename(ruta)} ({tablas[t_idx]})"
            else: return
            self.reset_estados()
            self.mostrar_info_basica()
        except Exception as e: print(f"Error al cargar: {e}")

    def ui_seleccionar_columnas(self):
        print("\n==============================\nSelección de Columnas\n==============================\nColumnas disponibles:")
        columnas = self.df.columns.tolist()
        for i, col in enumerate(columnas): print(f"  [{i+1}] {col}")
        try:
            feat_input = input("\nIngrese los números de las features (comas): ")
            target_input = input("\nIngrese el número del target: ")
            
            f_idx = [int(x.strip()) - 1 for x in feat_input.split(',')]
            t_idx = int(target_input.strip()) - 1
            if t_idx in f_idx: raise ValueError()

            self.features = [columnas[i] for i in f_idx]
            self.target = columnas[t_idx]
            self.df_original = self.df.copy()
            self.reset_estados()
            self.estados['seleccion_columnas'] = True
            print(f"\nSelección guardada: Features = {self.features}, Target = '{self.target}'")
        except: print("⚠ Error en la selección.")

    def ui_faltantes(self):
        print("\n==============================\nManejo de Valores Faltantes\n==============================")
        cols = self.features + [self.target]
        con_nulos = self.df[cols].columns[self.df[cols].isnull().any()].tolist()
        if not con_nulos:
            print("No se han detectado valores faltantes en las columnas seleccionadas.\nNo es necesario aplicar ninguna estrategia.")
            self.estados['valores_faltantes'] = True
            return
        
        print("Se han detectado valores faltantes:")
        for c in con_nulos: print(f"  - {c}: {self.df[c].isnull().sum()} faltantes")
        print("\n  [1] Eliminar filas\n  [2] Rellenar media\n  [3] Rellenar mediana\n  [4] Rellenar moda\n  [5] Valor constante\n  [6] Volver")
        op = input("Opción: ")
        if op in ['1','2','3','4','5']:
            val = input("Valor constante (si aplica): ") if op == '5' else None
            if val: val = float(val) if '.' in val else int(val)
            self.df = DataTransformer.manejar_faltantes(self.df, con_nulos, op, val)
            print("Valores gestionados correctamente.")
            self.estados['valores_faltantes'] = True

    def ui_categoricas(self):
        print("\n==============================\nTransformación de Categóricos\n==============================")
        cat_cols = self.df[self.features].select_dtypes(include=['object', 'category']).columns.tolist()
        if not cat_cols:
            print("No se detectaron columnas categóricas.\nNo es necesario transformar.")
            self.estados['trans_categorica'] = True
            return
            
        print("Columnas detectadas:"); [print(f"  - {c}") for c in cat_cols]
        print("\n  [1] One-Hot\n  [2] Label\n  [3] Volver")
        op = input("Opción: ")
        if op in ['1', '2']:
            self.df, self.features = DataTransformer.codificar_categoricas(self.df, self.features, cat_cols, op)
            print(f"Transformación completada.")
            self.estados['trans_categorica'] = True

    def ui_normalizar(self):
        print("\n==============================\nNormalización\n==============================")
        num_cols = self.df[self.features].select_dtypes(include=['number']).columns.tolist()
        if not num_cols:
            print("No hay numéricas.\nNo es necesario normalizar.")
            self.estados['normalizacion'] = True
            return
        print("Columnas detectadas:"); [print(f"  - {c}") for c in num_cols]
        print("\n  [1] Min-Max\n  [2] Z-score\n  [3] Volver")
        op = input("Opción: ")
        if op in ['1', '2']:
            self.df = DataTransformer.aplicar_escalado(self.df, num_cols, op)
            print("Normalización completada.")
            self.estados['normalizacion'] = True

    def ui_atipicos(self):
        print("\n==============================\nValores Atípicos\n==============================")
        num_cols = self.df[self.features].select_dtypes(include=['number']).columns.tolist()
        dict_atipicos, mascaras = DataTransformer.detectar_atipicos(self.df, num_cols)
        
        if not dict_atipicos:
            print("No se detectaron atípicos.\nNo es necesario aplicar estrategias.")
            self.estados['atipicos'] = True
            return
            
        print("Atípicos detectados:")
        for k,v in dict_atipicos.items(): print(f"  - {k}: {v} atípicos")
        print("\n  [1] Eliminar filas\n  [2] Reemplazar mediana\n  [3] Mantener\n  [4] Volver")
        op = input("Opción: ")
        if op in ['1','2']:
            self.df = DataTransformer.resolver_atipicos(self.df, mascaras, op)
            print("Atípicos gestionados.")
            self.estados['atipicos'] = True
        elif op == '3':
            print("Mantenidos sin cambios.")
            self.estados['atipicos'] = True

    def ui_visualizar(self):
        num_cols = self.df[self.features].select_dtypes(include=['number']).columns.tolist()
        print("\n==============================\nVisualización\n==============================\n  [1] Resumen estadístico\n  [2] Histogramas\n  [3] Dispersión (Antes/Después)\n  [4] Heatmap\n  [5] Volver")
        op = input("Opción: ")
        
        if op == '1':
            print(f"\n{'Variable':<15} | {'Media':<10} | {'Mediana':<10} | {'Desviación':<15}")
            print("-" * 55)
            for col in num_cols:
                m, md, sd = round(self.df[col].mean(), 2), round(self.df[col].median(), 2), round(self.df[col].std(), 2)
                print(f"{col:<15} | {str(m):<10} | {str(md):<10} | {str(sd):<15}")
            self.estados['visualizacion'] = True
        elif op == '2' and num_cols:
            DataVisualizer.mostrar_histogramas(self.df, num_cols)
            self.estados['visualizacion'] = True
        elif op == '3':
            c_orig = self.df_original.select_dtypes(include=['number']).columns.tolist()
            c_comun = [c for c in num_cols if c in c_orig]
            if len(c_comun) >= 2:
                DataVisualizer.mostrar_dispersion(self.df_original, self.df, c_comun[0], c_comun[1])
                self.estados['visualizacion'] = True
        elif op == '4' and len(num_cols) > 1:
            DataVisualizer.mostrar_heatmap(self.df, num_cols)
            self.estados['visualizacion'] = True

    def ui_exportar(self):
        if not (self.is_preprocesado_ok() and self.estados['visualizacion']):
            return print("\n==============================\nExportación\n==============================\nNo es posible exportar sin completar el preprocesado y la visualización.")
        
        print("\n==============================\nExportación\n==============================\n  [1] CSV\n  [2] Excel\n  [3] Volver")
        op = input("Opción: ")
        if op in ['1', '2']:
            nombre = input("Nombre de archivo (sin extensión): ").strip()
            if op == '1': DataIO.exportar_csv(self.df, f"{nombre}.csv")
            if op == '2': DataIO.exportar_excel(self.df, f"{nombre}.xlsx")
            print("Datos exportados correctamente.")
            self.estados['exportacion'] = True

if __name__ == "__main__":
    app = PipelineConsoleUI()
    app.menu_principal()