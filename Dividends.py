import pandas as pd

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

    def getDividendFromYearAndMonthExceptForTreasure(self, month, year):
        if 'Ano' in self.excel.columns and 'Mês' in self.excel.columns:
            rows = self.excel[(self.excel['Ano'] == year) & (self.excel['Mês'] == month) & (not self.excel['Ativo'].str.contains('Tesouro'))] 
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