'''
LECTURA DE ARCHIVOS EXPORTADOS POR BSALE
'''

# Importaciones
import pandas as pd


# Funciones
def lectura(archivo):
    dataframe = pd.read_excel(archivo, engine='openpyxl', header=5)
    return dataframe




