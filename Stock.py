import pandas as pd
from Files import StockPath


class Stock:
  list = []
  listFile = None

  def __init__(self):
    self.initialize()

  def get(self):
    return self.list

  def initialize(self):
    self.listFile = pd.read_excel(StockPath)['Cod']
    
    for stockCode in self.listFile:
      self.list.append(stockCode)

  def get(self):
    return self.list

## myStock = Stock()
## print(myStock.get())