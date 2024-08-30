import pandas as pd
from Dividends import Dividends
from datetime import date

class Wallet:
    df = None
    investment_df = None
    dividends = None
    total = None
    monthlyProfitability = None

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
    
    def calculateTotalAppliedInMonth(self, month, year):
        try:
            # convert columns to numbers, if there aren't
            self.df['Ano'] = self.df['Ano'].astype(int)
            self.df['Mês'] = self.df['Mês'].astype(int)

            # filter transactions up to the specified month/year
            filtered_df = self.df[(self.df['Ano'] < year) | 
                                ((self.df['Ano'] == year) & (self.df['Mês'] <= month))]

            # save all sold/bought transacctions up to the specified
            sold = filtered_df[filtered_df['Tipo de Movimentação'] == 'Venda']
            bought = filtered_df[filtered_df['Tipo de Movimentação'] == 'Compra']

            # group by negotiation code, summing quantity and price
            soldGrouped = sold.groupby('Código de Negociação')[['Quantidade', 'Valor']].sum().reset_index()
            boughtGrouped = bought.groupby('Código de Negociação')[['Quantidade', 'Valor']].sum().reset_index()

            # calculate avg price for sell/buy
            avg = (boughtGrouped['Valor'] / boughtGrouped['Quantidade']).round(2)
            avgSold = (soldGrouped['Valor'] / soldGrouped['Quantidade']).round(2)

            # Inser individual avg price in both df
            boughtGrouped['Preço Médio'] = avg
            soldGrouped['Preço Médio'] = avgSold

            # merge both df to secure itself to have all the negotiation codes included
            self.investment_df = pd.merge(boughtGrouped, soldGrouped, on='Código de Negociação', how='outer', suffixes=('_buy', '_sell'))

            # replace NaN with 0
            self.investment_df.fillna(0, inplace=True)

            # calculate quantity and value
            self.investment_df['Quantidade'] = self.investment_df['Quantidade_buy'] - self.investment_df['Quantidade_sell']
            self.investment_df['Valor'] = self.investment_df['Valor_buy'] - self.investment_df['Valor_sell']
            self.investment_df['Preço Médio'] = self.investment_df['Preço Médio_buy']

            # Remove not necessary columns
            self.investment_df = self.investment_df[self.investment_df['Quantidade'] != 0]
            self.investment_df = self.investment_df[['Código de Negociação', 'Quantidade', 'Valor', 'Preço Médio']]

            # calculate the total value invested up to the specified month/year
            return self.investment_df['Valor'].sum()

        except Exception as e:
            print(f'Erro: Não foi possível calcular o patrimônio. {e}')


    def getMonthlyProfitability(self, month, year):  
        try:
            if month == None:
                # get today's date
                today = date.today()
                # call a function to calculate the total applied
                totalAppliedUpToSpecifiedMonth = self.calculateTotalAppliedInMonth(month, year)
                
                # call the function to calculate the monthly profitability in Dividends class
                self.monthlyProfitability = self.dividends.getMonthlyProfitability(today.day, today.year, totalAppliedUpToSpecifiedMonth)
            elif type(month) is int or type(month) is float:
                self.monthlyProfitability = self.dividends.getMonthlyProfitability(month, year, self.total)
            else:
                raise Exception('Error: invalid type of month and getting todays date.')
            
            return print(f'Rentabilidade mensal: {self.monthlyProfitability.round(3)} %')
            
        except Exception as e:
            return print('Error: cannot calculate the monthly profitability.')

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
