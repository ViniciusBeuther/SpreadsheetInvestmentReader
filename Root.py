from Wallet import Wallet

transactionFile = '../src/assets/Negociações.xlsx'
dividendTransactions = '../src/assets/Dividendos Recebidos.xlsx'

wallet = Wallet(transactionFile, dividendTransactions)
#wallet.initialize()

while True:
    print('=-=-=-=-=-=-=-=-=-= CENTRAL DE INVESTIMENTOS =-=-=-=-=-=-=-=-=-=')
    print('1- Ver carteira')
    print('2- Ver total investido')
    print('3- Ver dividendos')
    print('4- Ver dividendos do mês')
    print('9- Sair')

    option = int(input('Opção Desejada: '))

    if option == 9:
        break

    elif option == 1:
        print('=-=-=-=-=-=-=-=-=-= CARTEIRA DE INVESTIMENTOS =-=-=-=-=-=-=-=-=-=')
        print(wallet.getInvestmentDf())
        print('\n\n')
    
    elif option == 2:
        print('=-=-=-=-=-=-=-=-=-= PATRIMÔNIO =-=-=-=-=-=-=-=-=-=')
        print('TOTAL INVESTIDO: R$ ', wallet.getTotal())
        print('\n')

    elif option == 3:
        print(wallet.getDividends())

    elif option == 4:
        wallet.dividends.getDividendFromYearAndMonth(5, 2024)

    else:
        print('Opção Inválida')