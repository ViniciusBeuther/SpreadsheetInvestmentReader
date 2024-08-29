import pandas as pd

class Dividends:
    monthlyProfitability = None
    excel = None
    def __init__(self, dividendTransactions):
        self.initialize(dividendTransactions)
    
    def initialize(self, dividendTransactions):
        self.excel = pd.read_excel(dividendTransactions)
        self.resumeProduct()

    def getDf(self):
        return print(self.excel)
    
    def getDividendFromYearAndMonth(self, month, year):
        if 'Ano' in self.excel.columns and 'Mês' in self.excel.columns:
            rows = self.excel[(self.excel['Ano'] == year) & (self.excel['Mês'] == month)] 
            print('Total: R$ ', rows['Valor líquido'].sum())
        else:
            print(f"'Year' or 'Month' column not found in DataFrame.")

    def resumeProduct(self):
        try:
            product_code = self.excel['Produto'].str.split('-').str[0]
            self.excel.insert(1, 'Cód. Ativo', product_code)
            self.excel.drop('Produto', axis=1, inplace=True)
        
        except Exception as e:
            return print('Error: Resuming codes. Check Dividends Class')
        
    def getMonthlyProfitability(self, month, year, totalApplied):
        try:
            if 'Ano' in self.excel.columns and 'Mês' in self.excel.columns:
                rows = self.excel[(self.excel['Ano'] == year) & (self.excel['Mês'] == month)] 
                self.monthlyProfitability = rows['Valor líquido'].sum()
                
                profitabilityPercentage = (self.monthlyProfitability * 100) / totalApplied
                return profitabilityPercentage

            else:
                print(f"'Year' or 'Month' not found in DataFrame.")

        except Exception as e:
            return print('Error: cannot calculate the monthly profitability.')