'''
LECTURA DE ARCHIVOS EXPORTADOS POR BSALE
'''

# Importaciones
import pandas as pd


# Funciones
def lectura(archivo, header):
    dataframe = pd.read_excel(archivo, engine='openpyxl', header=header)
    return dataframe




