from Wallet import Wallet
from GlobalFunctions import chooseMonth

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
        months = ['1-Janeiro', '2-Fevereiro', '3-Março', '4-Abril', '5-Maio', '6-Junho', '7-Julho', '8-Agosto', '9-Setembro', '10-Outubro', '11-Novembro', '12-Dezembro']
        
        print('=-=-=-=-=-=-=-=-=-= MESES =-=-=-=-=-=-=-=-=-=')
        # display all months as option
        for month in months:
            print(month)
        #call a function to get the month selected
        monthSelected = chooseMonth()
        
        try:
            wallet.dividends.getDividendFromYearAndMonth(monthSelected, 2024)
        except Exception as e:
            print('Erro: Algo deu errado.')

    elif option == 5:
        wallet.calculateAmountAppliedUpToDate(2,2024)
        pass

    else:
        print('Opção Inválida')