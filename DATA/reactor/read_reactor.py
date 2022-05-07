import openpyxl
from src.Reactor import Cascade


def read_reactor_from_xlsx(folder='./DATA/reactor', filename='Mol_Reactor.xlsx') -> Cascade:
    xlsx = openpyxl.load_workbook(f'{folder}/{filename}', data_only=True)
    sheet = xlsx.active

    cascade = Cascade(filename)

    for row_cell in sheet.iter_rows(min_row=1, max_row=1, min_col=2, max_col=9, values_only=True):
        titles = [title for title in row_cell]

    for reactor in sheet.iter_rows(min_row=2, min_col=2, max_col=9, values_only=True):
        parameters = {key: value for key, value in zip(titles, reactor)}
        cascade.add_reactor(reactor[0], parameters)

    return cascade
