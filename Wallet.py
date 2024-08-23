import pandas as pd
from Dividends import Dividends

class Wallet:
    df = None
    investment_df = None
    dividends = None
    total = None

    def __init__(self, transactionFile, dividendTransactions):
        self.df = pd.read_excel(transactionFile)
        self.investment_df = self.calculateAmount()
        self.total = 0.00
        self.initialize(dividendTransactions)
    
    def initialize(self, dividendTransactions):
        self.calculateAmount()
        self.dividends = Dividends(dividendTransactions)

    def getInvestmentDf(self):
        return self.investment_df
    
    def getTotal(self):
        return self.total
    
    def getDividends(self):
        return self.dividends.getDf()

    def calculateAmount(self):
        try:
            # Save all transaction bought and sold
            sold = self.df[self.df['Tipo de Movimentação'] == 'Venda']
            bought = self.df[self.df['Tipo de Movimentação'] == 'Compra']

            # Group them by negotiation code, summing the quantity and value
            soldGrouped = sold.groupby('Código de Negociação')[['Quantidade', 'Valor']].sum().reset_index()
            boughtGrouped = bought.groupby('Código de Negociação')[['Quantidade', 'Valor']].sum().reset_index()

            # Calculate the average price and insert it into the data frame
            avg = (boughtGrouped['Valor'] / boughtGrouped['Quantidade']).round(2)
            avgSold = (soldGrouped['Valor'] / soldGrouped['Quantidade']).round(2)

            # Insert the individual average price in both df
            boughtGrouped['Preço Médio'] = avg
            soldGrouped['Preço Médio'] = avgSold

            # Merge both DataFrames to ensure all negotiation codes are included
            self.investment_df = pd.merge(boughtGrouped, soldGrouped, on='Código de Negociação', how='outer', suffixes=('_buy', '_sell'))

            # Fill NaN values with 0 for subtraction
            self.investment_df.fillna(0, inplace=True)

            # Calculate net quantity and value
            self.investment_df['Quantidade'] = self.investment_df['Quantidade_buy'] - self.investment_df['Quantidade_sell']
            self.investment_df['Valor'] = self.investment_df['Valor_buy'] - self.investment_df['Valor_sell']
            self.investment_df['Preço Médio'] = self.investment_df['Preço Médio_buy']

            # Drop unnecessary columns
            self.investment_df = self.investment_df[self.investment_df['Quantidade'] != 0]
            self.investment_df = self.investment_df[['Código de Negociação', 'Quantidade', 'Valor', 'Preço Médio']]
            self.total = self.investment_df['Valor'].sum()

        except Exception as e:
            print(f'Erro: Não foi possível calcular o patrimônio. {e}')
