import openpyxl

from src.Reactor import Cascade


FOLDER = './DATA/reactor'
MIN_COL = 2
MAX_COL = 8


def read_reactor_from_xlsx(filename='Mol_Furnace.xlsx') -> Cascade:
    xlsx = openpyxl.load_workbook(f'{FOLDER}/{filename}', data_only=True)
    sheet = xlsx.active

    cascade = Cascade(filename)

    for row in sheet.iter_rows(
            min_row=2, min_col=MIN_COL, max_col=MAX_COL, values_only=True
    ):
        name, reactor = row[0], row[1:]
        parameters = {
            'temp_in': reactor[0],
            'temp_out': reactor[1],
            'press_in': reactor[2],
            'press_out': reactor[3],
            'volume': reactor[4],
            'steps': reactor[5]
        }
        cascade.add_reactor(name, parameters)
    return cascade
