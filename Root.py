from Wallet import Wallet
from GlobalFunctions import chooseMonth, clearTerminal

transactionFile = 'C:/Users/vinic/Downloads/PROJETOS DE DESENVOLVIMENTO/Controle de Rendimento/assets//Negociações.xlsx'
dividendTransactions = 'C:/Users/vinic/Downloads/PROJETOS DE DESENVOLVIMENTO/Controle de Rendimento/assets/Dividendos Recebidos.xlsx'

wallet = Wallet(transactionFile, dividendTransactions)
#wallet.initialize()

while True:
    print('=-=-=-=-=-=-=-=-=-= CENTRAL DE INVESTIMENTOS =-=-=-=-=-=-=-=-=-=')
    print('1- Ver carteira')
    print('2- Ver total investido')
    print('3- Ver dividendos totais')
    print('4- Ver dividendos de um mês específico')
    print('5- Ver rentabilidade mensal')
    print('6- Ver distribuição de carteira')
    print('9- Sair')

    option = int(input('Opção Desejada: '))

    if option == 9:
        break

    elif option == 1:
        clearTerminal()
        print('=-=-=-=-=-=-=-=-=-= CARTEIRA DE INVESTIMENTOS =-=-=-=-=-=-=-=-=-=')
        print(wallet.getInvestmentDf())
        print('\n\n')
    
    elif option == 2:
        clearTerminal()
        print('=-=-=-=-=-=-=-=-=-= PATRIMÔNIO =-=-=-=-=-=-=-=-=-=')
        print('TOTAL INVESTIDO: R$ ', wallet.getTotal())
        print('DIVIDENDOS RECEBIDOS: R$ ', wallet.getDividends())
        print('\n')

    elif option == 3:
        clearTerminal()
        print(wallet.getDividends())

    elif option == 4:
        clearTerminal()

        #call a function to get the month selected
        monthSelected = chooseMonth()
        
        try:
            wallet.dividends.getDividendFromYearAndMonth(monthSelected, 2024)
        except Exception as e:
            print('Erro: Algo deu errado.')

    elif option == 5:
        clearTerminal()
        currentYear = 2024
        while True:
            monthSelected = chooseMonth()
            if monthSelected == 0:
                break
            else:
                totalUpToSelectedMonth = wallet.calculateAmountAppliedUpToDateExceptTreasure(monthSelected, currentYear)
                #dividendsReceiptInMonthSelected = wallet.dividends.getDividendFromYearAndMonth(monthSelected, currentYear)
                dividendsReceiptInMonthSelected = wallet.dividends.getDividendFromYearAndMonth(monthSelected, currentYear)

                print('total investido até o Mês: ', totalUpToSelectedMonth)
                print('total recebido de div no mês: ', dividendsReceiptInMonthSelected)
                print(f'Rendimento de {monthSelected}: { ((dividendsReceiptInMonthSelected * 100) / totalUpToSelectedMonth).round(2)}')
                break

    elif option == 6:
        print('\n\n\n\n\n\n')
        wallet.getDistribution()

    else:
        print('Opção Inválida, tente novamente')