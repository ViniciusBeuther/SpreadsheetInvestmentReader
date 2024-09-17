import pandas as pd
from Wallet import Wallet

class Dividends:
    def __init__(self, file, transactionFile):
        self.df = pd.read_excel(file)
        self.df_transactions = pd.read_excel(transactionFile)
        self.resumeProduct()
        self.fiiCodes = [
            'CACR11',
            'BPFF11',
            'AFHI11',
            'AJFI11',
            'ALZR11',
            'RZAT11',
            'FATN11',
            'ARRI11',
            'AIEC11',
            'BARI11',
            'BCFF11',
            'BRCR11',
            'BCIA11',
            'BCRI11',
            'BLMG11',
            'BRCO11',
            'BROF11',
            'BTAL11',
            'BTCI11',
            'BTRA11',
            'BTLG11',
            'CPFF11',
            'CPTS11',
            'CLIN11',
            'CYCR11',
            'DEVA11',
            'VRTA11',
            'GTWR11',
            'GGRC11',
            'GARE11',
            'HABT11',
            'HCTR11',
            'HGBS11',
            'HGCR11',
            'HGFF11',
            'HGLG11',
            'HGPO11',
            'HGRE11',
            'HGRU11',
            'HTMX11',
            'HSAF11',
            'HSLG11',
            'HSML11',
            'HFOF11',
            'IRDM11',
            'JSAF11',
            'JSRE11',
            'KISU11',
            'KNRI11',
            'KCRE11',
            'KNHF11',
            'KNHY11',
            'KNIP11',
            'KNCR11',
            'KNSC11',
            'KFOF11',
            'KORE11',
            'LGCP11',
            'MALL11',
            'MCCI11',
            'MCHY11',
            'MXRF11',
            'MFII11',
            'NCHB11',
            'OUJP11',
            'PATL11',
            'PLCR11',
            'PORD11',
            'RBRL11',
            'RBRX11',
            'RBRY11',
            'RBRP11',
            'RBRF11',
            'RBRR11',
            'RECR11',
            'RECT11',
            'RBFF11',
            'RCRB11',
            'RBVA11',
            'RZAK11',
            'RZTR11',
            'SARE11',
            'TRBL11',
            'SPXS11',
            'SNCI11',
            'SNFF11',
            'TEPP11',
            'TGAR11',
            'TVRI11',
            'TORD11',
            'TRXF11',
            'URPR11',
            'VGHF11',
            'VGIP11',
            'VGIR11',
            'CVBI11',
            'LVBI11',
            'PVBI11',
            'RVBI11',
            'VCJR11',
            'VSLH11',
            'VIUR11',
            'VILG11',
            'VINO11',
            'VISC11',
            'WHGR11',
            'XPCI11',
            'XPIN11',
            'XPLG11',
            'XPML11',
            'XPPR11',
            'XPSF11',
        ]

    def setFiiCodes(self):
        dfFii = pd.read_excel('./FII codes.xlsx')
        self.fiiCodes = dfFii
        print(self.fiiCodes)

    def show(self):
        print(self.df)  
    
    def getDividendFromYearAndMonth(self, year, month):
        if 'Ano' in self.df.columns and 'Mês' in self.df.columns:
            rows = self.df[(self.df['Ano'] == year) & (self.df['Mês'] == month)] 
            print('Total: ', rows['Valor líquido'].sum())
        else:
            print(f"'Ano' or 'Mês' column not found in DataFrame.")

    def resumeProduct(self):
        stocks = self.df['Produto'].str.split('-').str[0]
        self.df.insert(1, 'Cód. Ativo', stocks)
        self.df.drop('Produto', axis=1, inplace=True)
        #self.totalOfDividendsReceipt()

    def totalOfDividendsReceipt(self):
        grouped = self.df.groupby('Cód. Ativo')['Valor líquido'].sum().reset_index()
        #print(grouped.sort_values(by='Valor líquido'))
        print(grouped.sort_values('Valor líquido', ascending=False))
        print('Total Recebido de Juros: R$ ', grouped['Valor líquido'].sum())


dividendsXLS = './Dividendos Recebidos.xlsx'
transactionsXLS = './Negociações.xlsx'
df = Dividends(dividendsXLS, transactionsXLS)

#df.resumeProduct()
#df.getDividendFromYearAndMonth(2024, 6) 
df.totalOfDividendsReceipt()

