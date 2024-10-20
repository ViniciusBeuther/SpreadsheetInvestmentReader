import pandas as pd

class FIIs:
  list = []
  listFile = '../assets/fundosImobiliariosListadosNaB3.xlsx'
  def __init__(self):
    pass

  def setFiiCodes(self):
    self.listFile = pd.read_excel(self.listFile)

fii = FIIs()
fii.setFiiCodes()