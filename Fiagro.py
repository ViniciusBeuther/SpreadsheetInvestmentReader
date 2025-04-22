import pandas as pd
import os
from Files import FiiAgroList

# excelPath = 'C:/Users/vinic/Downloads/PROJETOS DE DESENVOLVIMENTO/Controle de Rendimento/assets/FIAGRO.xlsx'

class Fiagro:
  list = []

  def __init__(self):
    self.initialize()

  def initialize(self):
    self.listFile = pd.read_excel(FiiAgroList)['Cod']
    for asset in self.listFile:
      self.list.append(asset)

  def get(self):
    return self.list
  
## fiagro = Fiagro()
## print(fiagro.get())