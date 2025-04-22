import pandas as pd
from Files import DividendsList

class Dividends:
    excel = None
    def __init__(self, dividendTransactions):
        self.initialize(dividendTransactions)
    
    def initialize(self, dividendTransactions):
        self.excel = pd.read_excel(dividendTransactions)
        self.resumeProduct()

    def getDf(self):
        return print(self.excel)
    
    def getTotalDividends(self):
        return self.excel['Valor líquido'].sum()
    
    def getDividendFromYearAndMonth(self, month, year):
        if 'Ano' in self.excel.columns and 'Mês' in self.excel.columns:
            rows = self.excel[(self.excel['Ano'] == year) & (self.excel['Mês'] == month)] 
            print('Total: R$ ', rows['Valor líquido'].sum())
            totalReceipt = rows['Valor líquido'].sum()

            return totalReceipt
        else:
            print(f"'Year' or 'Month' column not found in DataFrame.")

    def getDividendFromYearAndMonth(self, month, year):
        if 'Ano' in self.excel.columns and 'Mês' in self.excel.columns:
            rows = self.excel[(self.excel['Ano'] == year) & (self.excel['Mês'] == month)] 
            print('Total: R$ ', rows['Valor líquido'].sum())
            totalReceipt = rows['Valor líquido'].sum()   
            return totalReceipt
        else:
            print(f"'Year' or 'Month' column not found in DataFrame.")

    def resumeProduct(self):
        try:
            product_code = self.excel['Produto'].str.split('-').str[0]
            self.excel.insert(1, 'Cód. Ativo', product_code)
            self.excel.drop('Produto', axis=1, inplace=True)
        
        except Exception as e:
            return print('Error: Resuming codes. Check Dividends Class')
        

    def getDividendsByYear(self, year):
        try:
            df = pd.read_excel(DividendsList)
            # Filter by year provided in DF 
            df_year = df[df['Ano'] == year]
            df_year['Código'] = df_year['Produto'].str.split(' - ').str[0]
            # print(df_year['Código'])

            # Sort values by code and total received
            df_year.sort_values(by=["Código","Valor líquido"])
            
            # Group by product and sum the liquid total
            grouped = df_year.groupby('Código')['Valor líquido'].sum().reset_index()
            
            # Rename the column
            grouped.rename(columns={'Valor líquido': 'Total de Proventos'}, inplace=True)

            # Return a print
            return print(grouped)

        except Exception as e:
            print(f'Erro ao calcular os proventos do ano {year}: {e}')
            return pd.DataFrame()

    def getDividendsByYearAndType(self, year):
        try:
            df = pd.read_excel(DividendsList)
            df_year = df[df['Ano'] == year].copy()

            # Get the asset code
            df_year['Código'] = df_year['Produto'].str.split(' - ').str[0]

            # classify provent type
            def classify(event):
                event = event.lower()
                if 'dividendo' in event or 'rendimento' in event:
                    return 'Dividendo/Rendimento'
                elif 'juros' in event:
                    return 'Juros/JCP'
                else:
                    return 'Outro'

            df_year['Categoria'] = df_year['Tipo de Evento'].apply(classify)
            df_year.sort_values(by=['Código', 'Valor líquido'])
            # Group by code and category
            grouped = df_year.groupby(['Código', 'Categoria'])['Valor líquido'].sum().reset_index()
            grouped.rename(columns={'Valor líquido': 'Total'}, inplace=True)

            return print(grouped)

        except Exception as e:
            print(f'Erro ao separar os proventos do ano {year}: {e}')
            return pd.DataFrame()
