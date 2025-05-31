import pandas as pd
from Dividends import Dividends
from FIIs import FIIs
from Stock import Stock
from Fiagro import Fiagro
import re
from Files import FiiList

# fiiListPath = '/Users/viniciusbeuther/Documents/Development/Personal/SpreadsheetInvestmentReader/assets/fundosImobiliariosListadosNaB3.xlsx'
fiiListPath = FiiList

class Wallet:
    df = None
    investment_df = None
    dividends = None
    total = None
    stockTupleList = []
    fiagroTupleList = []
    fiiTupleList = []

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
            # Ensure the date is in datetime format and sort by it
            self.df['Data do Negócio'] = pd.to_datetime(self.df['Data do Negócio'], dayfirst=True)
            self.df.sort_values(by='Data do Negócio', inplace=True)

            result_assets = []

            for code in self.df['Código de Negociação'].unique():
                asset_df = self.df[self.df['Código de Negociação'] == code].copy()
                portfolio = []  # each item will be a tuple: (quantity, total_value)

                for _, row in asset_df.iterrows():
                    movement_type = row['Tipo de Movimentação']
                    quantity = row['Quantidade']
                    value = row['Valor']

                    if movement_type == 'Compra':
                        portfolio.append((quantity, value))
                    elif movement_type == 'Venda':
                        quantity_to_sell = quantity
                        while quantity_to_sell > 0 and portfolio:
                            lot_quantity, lot_value = portfolio[0]
                            if lot_quantity <= quantity_to_sell:
                                quantity_to_sell -= lot_quantity
                                portfolio.pop(0)
                            else:
                                # Sell part of the lot
                                remaining_ratio = (lot_quantity - quantity_to_sell) / lot_quantity
                                new_value = lot_value * remaining_ratio
                                portfolio[0] = (lot_quantity - quantity_to_sell, new_value)
                                quantity_to_sell = 0

                total_quantity = sum(l[0] for l in portfolio)
                total_value = sum(l[1] for l in portfolio)
                average_price = round(total_value / total_quantity, 2) if total_quantity > 0 else 0

                if total_quantity > 0:
                    result_assets.append({
                        'Código de Negociação': code,
                        'Quantidade': total_quantity,
                        'Valor': round(total_value, 2),
                        'Preço Médio': average_price
                    })

            self.investment_df = pd.DataFrame(result_assets)
            self.total = self.investment_df['Valor'].sum()

            # Add "Tipo" column if it doesn't exist
            if 'Tipo' not in self.investment_df.columns:
                self.investment_df['Tipo'] = None

            list_of_fiis = FIIs().get()
            list_of_stocks = Stock().get()
            list_of_fiagro = Fiagro().get()

            for index, row in self.investment_df.iterrows():
                simple_code = row['Código de Negociação'][:4]
                stock_code = row['Código de Negociação']

                if len(row['Código de Negociação']) >= 6:
                    if row['Código de Negociação'][4:7] == '11F':
                        stock_code = row['Código de Negociação'][:6]
                    elif bool(re.search('[0-9]+F', row['Código de Negociação'][4:7])):
                        stock_code = row['Código de Negociação'][:5]
                    elif bool(re.search('.*Tesouro.*', row['Código de Negociação'])):
                        self.investment_df.at[index, 'Tipo'] = 'Tesouro Direto'

                if simple_code in list_of_fiis:
                    self.investment_df.at[index, 'Tipo'] = 'FII'
                elif stock_code in list_of_stocks:
                    self.investment_df.at[index, 'Tipo'] = 'Ação'
                elif stock_code in list_of_fiagro or simple_code in list_of_fiagro:
                    self.investment_df.at[index, 'Tipo'] = 'FIAGRO'

        except Exception as e:
            print(f'Error: Could not calculate the portfolio. {e}')



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

            return total 
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
        tempTable = self.investment_df[['Código de Negociação', 'Tipo', 'Valor']]
        self.fiiTupleList = []
        self.stockTupleList = []
        self.fiagroTupleList = []
        self.tesouroTupleList = []

        totalFii = 0
        totalFiagro = 0
        totalStock = 0
        totalTesouro = 0

        for _, row in tempTable.iterrows():
            tipo = row['Tipo']
            codigo = row['Código de Negociação']
            valor = row['Valor']

            if tipo == 'FII':
                self.fiiTupleList.append((codigo, valor))
                totalFii += valor
            elif tipo == 'FIAGRO':
                self.fiagroTupleList.append((codigo, valor))
                totalFiagro += valor
            elif tipo == 'Ação':
                self.stockTupleList.append((codigo, valor))
                totalStock += valor
            elif tipo == 'Tesouro Direto':
                self.tesouroTupleList.append((codigo, valor))
                totalTesouro += valor

        # Calcular percentuais
        stockPercent = (100 * totalStock) / self.total if self.total else 0
        fiiPercent = (100 * totalFii) / self.total if self.total else 0
        fiagroPercent = (100 * totalFiagro) / self.total if self.total else 0
        tesouroPercent = (100 * totalTesouro) / self.total if self.total else 0

        # Print (opcional)
        print('=-=-=-=-=-=-=-=-=-= DISTRIBUIÇÃO DE ATIVOS =-=-=-=-=-=-=-=-=-=')
        print(f'Total em ações: {stockPercent:.2f} % ($ {totalStock:.2f})')
        print(f'Total em Fundos Imobiliários: {fiiPercent:.2f} % ($ {totalFii:.2f})')
        print(f'Total em Fiagro: {fiagroPercent:.2f} % ($ {totalFiagro:.2f})')
        print(f'Total no Tesouro Direto: {tesouroPercent:.2f} % ($ {totalTesouro:.2f})')
        print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n\n\n')

        # Construir objeto de resposta
        returnObj = {
            "distribution": [
                {"type": "acao", "total": totalStock, "percentage": stockPercent},
                {"type": "fii", "total": totalFii, "percentage": fiiPercent},
                {"type": "fiagro", "total": totalFiagro, "percentage": fiagroPercent},
                {"type": "tesouro", "total": totalTesouro, "percentage": tesouroPercent},
            ]
        }
        # ,
        #     "details": {
        #         "acao": self.stockTupleList,
        #         "fii": self.fiiTupleList,
        #         "fiagro": self.fiagroTupleList,
        #         "tesouro": self.tesouroTupleList
        #     }

        return returnObj

        
        