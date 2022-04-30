import openpyxl
from src.Reactions import Reactions


def read_reactions_from_xlsx(folder='./DATA/reactions',
                             filename='example.xlsx'):
    xlsx = openpyxl.load_workbook(f'{folder}/{filename}', data_only=True)
    sheet = xlsx.active

    reactions = Reactions(filename)

    row_id = 1
    while True:
        id = sheet.cell(column=1, row=row_id).value
        if id is not None:
            parameters = {
                'id': id,
                'components': {},
                'divider': 0,
                'order': {},
                'A': 0,
                'E': 0,
                'n': 0,
                'equation': ''
            }

            for col in range(2, 6):
                name = sheet.cell(column=col, row=row_id).value
                coefficient = sheet.cell(column=col, row=row_id + 1).value
                order = sheet.cell(column=col, row=row_id + 2).value
                if name is not None:
                    parameters['components'][name] = coefficient
                    parameters['order'][name] = order

            for col in range(6, 8):
                parameter = sheet.cell(column=col, row=row_id).value
                value = sheet.cell(column=col, row=row_id + 2).value
                parameters[parameter] = value
            parameters['n'] = sum(parameters['order'].values())
            parameters['divider'] = sheet.cell(column=8, row=row_id + 1).value
            row_id += 4

            reactions.add_reaction(id, parameters)

        else:
            return reactions
