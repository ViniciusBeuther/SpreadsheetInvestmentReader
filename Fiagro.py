import pandas as pd

excelPath = 'C:/Users/vinic/Downloads/PROJETOS DE DESENVOLVIMENTO/Controle de Rendimento/assets/FIAGRO.xlsx'

class Fiagro:
  list = []

  def __init__(self):
    self.initialize()

  def initialize(self):
    self.listFile = pd.read_excel(excelPath)['Cod']
    for asset in self.listFile:
      self.list.append(asset)

  def get(self):
    return self.list
  
## fiagro = Fiagro()
## print(fiagro.get())