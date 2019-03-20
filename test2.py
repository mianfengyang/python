
from openpyxl import Workbook
wb = Workbook()
ws = wb.active
ws['A1'] = "用户目录"
ws['B1'] = "最新修改目录"
ws['C1'] = "最新修改时间"

list = [1,2,3,4,5,6]
ws.append(list)

wb.save("test.xlsx")