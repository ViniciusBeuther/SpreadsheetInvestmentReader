def chooseMonth():
    months = ['1-Janeiro', '2-Fevereiro', '3-Março', '4-Abril', '5-Maio', '6-Junho', '7-Julho', '8-Agosto', '9-Setembro', '10-Outubro', '11-Novembro', '12-Dezembro']

    print('=-=-=-=-=-=-=-=-=-= MESES =-=-=-=-=-=-=-=-=-=')
    # display all months as option
    for month in months:
        print(month)
    
    monthSelected = int(input('Qual mês você deseja (0 para sair):'))
    if monthSelected == 0:
        return 0
    elif monthSelected == 1:
        return 1
    elif monthSelected == 2:
        return 2
    elif monthSelected == 3:
        return 3
    elif monthSelected == 4:
        return 4
    elif monthSelected == 5:
        return 5
    elif monthSelected == 6:
        return 6
    elif monthSelected == 7:
        return 7
    elif monthSelected == 8:
        return 8
    elif monthSelected == 9:
        return 9
    elif monthSelected == 10:
        return 10
    elif monthSelected == 11:
        return 11
    elif monthSelected == 12:
        return 12
    else:
        print('Mês digitado é Inválido.')

def clearTerminal():
    for i in range(0,20):
        print('\n')