import easyquotation as eq
import openpyxl

excelfile = '/home/frank/project/doc/stock/mystock.xlsx'

class GetStocks:

    def __init__(self,code) -> None:
        self.code = code
    
    def getStockClosePrice(self):
        quotation = eq.use('sina')
        self.closePrice = quotation.real(self.code)[''+self.code+'']['close']
        return self.closePrice
    
    def getStockName(self):
        quotation = eq.use('sina')
        self.name = quotation.real(self.code)[''+self.code+'']['name']
        return self.name
    
    def printStockInfo(self):
        print('股票名称：'+self.getStockName())
        print('昨日收盘：'+str(self.getStockClosePrice()))
        
    def writeExcel(self):
        tableAll = openpyxl.load_workbook(excelfile)
        table = tableAll[''+self.name+'-'+self.code+'']
        table.cell(5,4,self.closePrice)
        tableAll.save(excelfile)
    

if __name__ == "__main__":
    stocklist = ['600809','600745']
    for i in stocklist:
        s1 = GetStocks(i)
        s1.printStockInfo()
        s1.writeExcel()
