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
        if id is None:
            break
        parameters = {'id': id}

        components = [col[0] for col in sheet.iter_cols(min_col=2, max_col=5,
                                                        min_row=row_id, max_row=row_id,
                                                        values_only=True) if col[0] is not None]
        coefficient = [col[0] for col in sheet.iter_cols(min_col=2, max_col=5,
                                                         min_row=row_id + 1, max_row=row_id + 1,
                                                         values_only=True) if col[0] is not None]
        order = [col[0] for col in sheet.iter_cols(min_col=2, max_col=5,
                                                   min_row=row_id + 2, max_row=row_id + 2,
                                                   values_only=True) if col[0] is not None]
        titles = [col[0] for col in sheet.iter_cols(min_col=6, max_col=7,
                                                    min_row=row_id, max_row=row_id,
                                                    values_only=True) if col[0] is not None]
        values = [col[0] for col in sheet.iter_cols(min_col=6, max_col=7,
                                                    min_row=row_id + 2, max_row=row_id + 2,
                                                    values_only=True) if col[0] is not None]

        for i, title in enumerate(titles):
            parameters[title] = values[i]
        parameters['balance'] = {key: value for key, value in zip(components, coefficient)}
        divider = sheet.cell(column=8, row=row_id + 1).value
        parameters['order'] = {key: value / divider for key, value in zip(components, order)}
        parameters['n'] = sum(parameters['order'].values())

        reactions.add_reaction(id, parameters)

        row_id += 4

    return reactions
