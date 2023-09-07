

    def analisis_rotacion_periodica(self):
        dataframe_ventas = self.procesador_dataframe_ventas_semanales()

        ventas_totales = dataframe_ventas
        dataframe_stock = self.procesador_dataframe_stock_historico()

        # Asegurarte de que la columna de fecha sea del tipo datetime
        dataframe_ventas.index = pd.to_datetime(dataframe_ventas.index)
        dataframe_stock['Fecha'] = pd.to_datetime(dataframe_stock['Fecha'])

        # Filtrar los dataframes para que solo contengan datos en el rango de self.f_inicio y self.f_fin
        dataframe_ventas = dataframe_ventas.loc[self.f_inicio:self.f_fin]
        dataframe_stock = dataframe_stock[(dataframe_stock['Fecha'] >= self.f_inicio) & (dataframe_stock['Fecha'] <= self.f_fin)]

        # Calcular la cantidad de meses y trimestres completos dentro del rango de fechas
        total_meses = (pd.to_datetime(self.f_fin).year - pd.to_datetime(self.f_inicio).year) * 12 + pd.to_datetime(self.f_fin).month - pd.to_datetime(self.f_inicio).month
        total_trimestres = total_meses // 3  # Esto dará el número de trimestres completos

        # Ventas y compras a nivel mensual
        ventas_mensuales = dataframe_ventas.resample('M').sum()
        #compras_mensuales = dataframe_stock[dataframe_stock['Tipo'] == 'Compra'].resample('M', on='Fecha').sum()

        # Ventas y compras a nivel trimestral
        ventas_trimestrales = dataframe_ventas.resample('Q').sum()
        #compras_trimestrales = dataframe_stock[dataframe_stock['Tipo'] == 'Compra'].resample('Q', on='Fecha').sum()

        # Ventas y compras a nivel anual
        ventas_anuales = dataframe_ventas.resample('A').sum()
        #compras_anuales = dataframe_stock[dataframe_stock['Tipo'] == 'Compra'].resample('A', on='Fecha').sum()

        # Aquí puedes imprimir los resultados o devolverlos, según lo necesites.
        if total_meses >= 1:
            print(f"Análisis para {total_meses} meses desde {self.f_inicio} hasta {self.f_fin}")
            print("Ventas mensuales:\n", ventas_mensuales)
            #rint("Compras mensuales:\n", compras_mensuales)

        if total_trimestres >= 1:
            print(f"Análisis para {total_trimestres} trimestres desde {self.f_inicio} hasta {self.f_fin}")
            print("Ventas trimestrales:\n", ventas_trimestrales)
            #print("Compras trimestrales:\n", compras_trimestrales)

        if pd.to_datetime(self.f_fin).year - pd.to_datetime(self.f_inicio).year >= 1:
            print(f"Análisis anual desde {self.f_inicio} hasta {self.f_fin}")
            print("Ventas anuales:\n", ventas_anuales)
            #print("Compras anuales:\n", compras_anuales)
