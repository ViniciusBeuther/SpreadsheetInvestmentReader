import pandas as pd

class FIIs:
  list = []
  listFile = '../assets/fundosImobiliariosListadosNaB3.csv'
  def __init__(self):
    pass

  def setFiiCodes(self):
    self.listFile = pd.read_csv(self.listFile)
    print(self.listFile)

fii = FIIs()
fii.setFiiCodes()