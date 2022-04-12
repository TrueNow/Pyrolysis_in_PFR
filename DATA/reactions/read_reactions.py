import openpyxl


def read_reactions_from_xlsx(folder='D:/Models_In_Python/Work_Model v4.0/DATA/reactions',
                             filename='example.xlsx'):
    """
    reactions = {
        id: {
            'ID': int,\n
            'Components': dict,\n
            'Divider': float,\n
            'Order': dict,\n
            'A': float,\n
            'E': float,\n
            'n': int,\n
            'equation': str,\n
        }
    }

    :return: All reactions from xlsx file
    :rtype: dict
    """

    file = f'{folder}/{filename}'
    xlsx = openpyxl.load_workbook(f'{file}', data_only=True)
    sheet = xlsx.active

    reactions = {}

    row_id = 1
    while True:
        id = sheet.cell(column=1, row=row_id).value
        if id is not None:
            reactions[id] = {
                'ID': id,
                'Components': {},
                'Divider': 0,
                'Order': {},
                'A': 0,
                'E': 0,
                'n': 0,
                'equation': ''
            }

            for col in range(2, 6):
                name = sheet.cell(column=col, row=row_id).value
                coefficient = sheet.cell(column=col, row=row_id + 1).value
                n = sheet.cell(column=col, row=row_id + 2).value
                if name is not None:
                    reactions[id]['Components'][name] = coefficient
                    reactions[id]['Order'][name] = n

            for col in range(6, 8):
                parameter = sheet.cell(column=col, row=row_id).value
                value = sheet.cell(column=col, row=row_id + 2).value
                reactions[id][parameter] = value
            reactions[id]['n'] = sum(reactions[id]['Order'].values())
            reactions[id]['Divider'] = sheet.cell(column=8, row=row_id + 1).value
            row_id += 4
        else:
            return reactions
