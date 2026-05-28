import matplotlib.pyplot as plt
import seaborn as sns

class DataVisualizer:
    """Responsable de renderizar gráficos."""
    @staticmethod
    def mostrar_histogramas(df, columnas):
        df[columnas].hist(bins=20, figsize=(12, 8), edgecolor='black')
        plt.suptitle("Histogramas de variables numéricas (Post-procesado)", fontsize=16)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def mostrar_dispersion(df_original, df_procesado, col_x, col_y):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        ax1.scatter(df_original[col_x], df_original[col_y], alpha=0.6, color='blue')
        ax1.set_title("Antes de la normalización")
        ax1.set_xlabel(col_x)
        ax1.set_ylabel(col_y)
        ax1.grid(True, linestyle='--', alpha=0.7)
        
        ax2.scatter(df_procesado[col_x], df_procesado[col_y], alpha=0.6, color='orange')
        ax2.set_title("Después del preprocesado")
        ax2.set_xlabel(col_x)
        ax2.set_ylabel(col_y)
        ax2.grid(True, linestyle='--', alpha=0.7)
        
        plt.suptitle(f"Comparación de Dispersión: {col_x} vs {col_y}", fontsize=16)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def mostrar_heatmap(df, columnas):
        plt.figure(figsize=(10, 8))
        sns.heatmap(df[columnas].corr(), annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
        plt.title("Heatmap de correlación de variables numéricas", fontsize=16)
        plt.tight_layout()
        plt.show()