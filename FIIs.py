import pandas as pd

excelPath = 'C:/Users/vinic/Downloads/PROJETOS DE DESENVOLVIMENTO/Controle de Rendimento/assets/fundosImobiliariosListadosNaB3.xlsx'

class FIIs:
  list = []

  def __init__(self):
    self.initialize()

  def get(self):
    return self.list

  def initialize(self):
    self.listFile = pd.read_excel(excelPath)['Código']
    for i in self.listFile:
      self.list.append(i)

fii = FIIs()
## print(fii.get())