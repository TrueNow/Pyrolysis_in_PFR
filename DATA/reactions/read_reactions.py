import openpyxl
from src.Reactions import Reactions


def read_reactions_from_xlsx(folder='./DATA/reactions',
                             filename='example.xlsx'):
    global titles, values, components, coefficient, order

    xlsx = openpyxl.load_workbook(f'{folder}/{filename}', data_only=True)
    sheet = xlsx.active

    reactions = Reactions(filename)

    row_id = 1
    while True:
        id = sheet.cell(column=1, row=row_id).value
        if id is None:
            break
        parameters = {'id': id}

        for row in [row_id, row_id + 1, row_id + 2]:
            for row_cells in sheet.iter_rows(min_col=2, max_col=5, min_row=row, max_row=row, values_only=True):
                if row == row_id:
                    components = [value for value in row_cells if value is not None]
                elif row == row_id + 1:
                    coefficient = [value for value in row_cells if value is not None]
                elif row == row_id + 2:
                    order = [value for value in row_cells if value is not None]

        for row in [row_id, row_id + 2]:
            for row_cells in sheet.iter_rows(min_col=6, max_col=7, min_row=row, max_row=row, values_only=True):
                if row == row_id:
                    titles = [value for value in row_cells if value is not None]
                elif row == row_id + 2:
                    values = [value for value in row_cells if value is not None]

        for i, title in enumerate(titles):
            parameters[title] = values[i]
        parameters['balance'] = {key: value for key, value in zip(components, coefficient)}
        divider = sheet.cell(column=8, row=row_id + 1).value
        parameters['order'] = {key: value / divider for key, value in zip(components, order)}
        parameters['n'] = sum(parameters['order'].values())

        print(parameters)
        reactions.add_reaction(id, parameters)

        row_id += 4

    return reactions
