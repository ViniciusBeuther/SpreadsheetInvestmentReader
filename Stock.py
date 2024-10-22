import pandas as pd

excelPath = 'C:/Users/vinic/Downloads/PROJETOS DE DESENVOLVIMENTO/Controle de Rendimento/assets/Acoes.xlsx'

class Stock:
  list = []
  listFile = None

  def __init__(self):
    self.initialize()

  def get(self):
    return self.list

  def initialize(self):
    self.listFile = pd.read_excel(excelPath)['Cod']
    
    for stockCode in self.listFile:
      self.list.append(stockCode)

  def get(self):
    return self.list

## myStock = Stock()
## print(myStock.get())