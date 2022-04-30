import openpyxl
from src.Reactor import Cascade


def read_reactor_from_xlsx(folder='./DATA/reactor',
                           filename='Mol_Reactor.xlsx'):
    xlsx = openpyxl.load_workbook(f'{folder}/{filename}', data_only=True)
    sheet = xlsx.active

    cascade = Cascade(filename)
    data = []

    for row in range(2, sheet.max_row + 1):
        name = sheet.cell(column=1, row=row).value
        parameters = {}
        for col in range(2, sheet.max_column + 1):
            try:
                parameters[sheet.cell(column=col, row=1).value] = float(sheet.cell(column=col, row=row).value)
            except ValueError:
                parameters[sheet.cell(column=col, row=1).value] = sheet.cell(column=col, row=row).value
        cascade.add_reactor(name, parameters)
        data.append([*parameters.values()])
    return cascade, data
