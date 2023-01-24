from openpyxl import Workbook

def save_p():
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'hello'
    worksheet.cell(row=1, column=1, value='hey')
    workbook.save('./test.xlsx')