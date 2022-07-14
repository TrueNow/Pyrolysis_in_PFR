import openpyxl
from src.Flow import Components

FOLDER = './DATA/components'
FILE = 'All_components.xlsx'


def read_components_from_xlsx(used_components: list) -> Components:
    file = f'{FOLDER}/{FILE}'

    xlsx = openpyxl.load_workbook(file, data_only=True)
    sheet = xlsx.active

    components = Components()

    for name, molar_mass, molecular, formula in sheet.iter_rows(min_row=2, min_col=1, max_col=4, values_only=True):
        if name is None:
            break
        if name in used_components:
            properties = {'molar_mass': molar_mass, 'molecular': molecular, 'formula': formula}
            components.add_component(name, properties)

    return components
