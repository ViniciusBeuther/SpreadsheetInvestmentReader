import pandas as pd
from Dividends import Dividends
import re

fiiListPath = '../assets/fundosImobiliariosListadosNaB3.csv'

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
        return self.dividends.getTotalDividends()

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

    def calculateAmountAppliedUpToDate(self, month, year):
        try:
            # Filter the DataFrame based on the specified year and month
            filtered_df = self.df[(self.df['Ano'] < year) | ((self.df['Ano'] == year) & (self.df['Mês'] <= month))]

            # Save all transactions bought and sold
            sold = filtered_df[filtered_df['Tipo de Movimentação'] == 'Venda']
            bought = filtered_df[filtered_df['Tipo de Movimentação'] == 'Compra']

            # Group them by negotiation code, summing the quantity and value
            soldGrouped = sold.groupby('Código de Negociação')[['Quantidade', 'Valor']].sum().reset_index()
            boughtGrouped = bought.groupby('Código de Negociação')[['Quantidade', 'Valor']].sum().reset_index()

            # Calculate the average price and insert it into the data frame
            avg_bought = (boughtGrouped['Valor'] / boughtGrouped['Quantidade']).round(2)
            avg_sold = (soldGrouped['Valor'] / soldGrouped['Quantidade']).round(2)

            # Insert the individual average price in both DataFrames
            boughtGrouped['Preço Médio'] = avg_bought
            soldGrouped['Preço Médio'] = avg_sold

            # Merge both DataFrames to ensure all negotiation codes are included.
            investment_df = pd.merge(boughtGrouped, soldGrouped, on='Código de Negociação', how='outer', suffixes=('_buy', '_sell'))

            # Fill NaN values with 0 for subtraction
            investment_df.fillna(0, inplace=True)

            # Calculate net quantity and value
            investment_df['Quantidade'] = investment_df['Quantidade_buy'] - investment_df['Quantidade_sell']
            investment_df['Valor'] = investment_df['Valor_buy'] - investment_df['Valor_sell']
            investment_df['Preço Médio'] = investment_df['Preço Médio_buy']

            # Drop assets with zero net quantity
            investment_df = investment_df[investment_df['Quantidade'] != 0]

            # Select relevant columns
            investment_df = investment_df[['Código de Negociação', 'Quantidade', 'Valor', 'Preço Médio']]
            
            # Calculate the total value
            total = investment_df['Valor'].sum()
            
            # Store the updated DataFrame and total value for further use
            self.investment_df = investment_df
            self.total = total

            #Debug variables
            #print('Remaining positions:', investment_df)
            #print(f'Total Investido até {month}/{year}: R$ {total}')

            return total  # Return the calculated total
        except Exception as e:
            print("Error in calculateAmountAppliedUpToDate method.\nDetails: ", e)
            return None

    # Calculate the amount just over the stocks and real state, not considering the government titles
    def calculateAmountAppliedUpToDateExceptTreasure(self, month, year):
        try:
            # Filter the DataFrame based on the specified year and month
            filtered_df = self.df[(self.df['Ano'] < year) | ((self.df['Ano'] == year) & (self.df['Mês'] <= month) & (self.df['Código de Negociação'].str.contains('Tesouro IPCA') == False))]
            print('filter: ', filtered_df)

            # Save all transactions bought and sold
            sold = filtered_df[filtered_df['Tipo de Movimentação'] == 'Venda']
            bought = filtered_df[filtered_df['Tipo de Movimentação'] == 'Compra']

            # Group them by negotiation code, summing the quantity and value
            soldGrouped = sold.groupby('Código de Negociação')[['Quantidade', 'Valor']].sum().reset_index()
            boughtGrouped = bought.groupby('Código de Negociação')[['Quantidade', 'Valor']].sum().reset_index()

            # Calculate the average price and insert it into the data frame
            avg_bought = (boughtGrouped['Valor'] / boughtGrouped['Quantidade']).round(2)
            avg_sold = (soldGrouped['Valor'] / soldGrouped['Quantidade']).round(2)

            # Insert the individual average price in both DataFrames
            boughtGrouped['Preço Médio'] = avg_bought
            soldGrouped['Preço Médio'] = avg_sold

            # Merge both DataFrames to ensure all negotiation codes are included.
            investment_df = pd.merge(boughtGrouped, soldGrouped, on='Código de Negociação', how='outer', suffixes=('_buy', '_sell'))

            # Fill NaN values with 0 for subtraction
            investment_df.fillna(0, inplace=True)

            # Calculate net quantity and value
            investment_df['Quantidade'] = investment_df['Quantidade_buy'] - investment_df['Quantidade_sell']
            investment_df['Valor'] = investment_df['Valor_buy'] - investment_df['Valor_sell']
            investment_df['Preço Médio'] = investment_df['Preço Médio_buy']

            # Drop assets with zero net quantity
            investment_df = investment_df[investment_df['Quantidade'] != 0]

            # Select relevant columns
            investment_df = investment_df[['Código de Negociação', 'Quantidade', 'Valor', 'Preço Médio']]
            
            # Calculate the total value
            total = investment_df['Valor'].sum()
            
            # Store the updated DataFrame and total value for further use
            self.investment_df = investment_df
            self.total = total

            #Debug variables
            #print('Remaining positions:', investment_df)
            #print(f'Total Investido até {month}/{year}: R$ {total}')

            return total  # Return the calculated total
        except Exception as e:
            print("Error in calculateAmountAppliedUpToDate method.\nDetails: ", e)
            return None

    def getDistribution(self):
        stockList = []
        fiiList = pd.read_csv( fiiListPath )
        print(fiiList)
        pass
