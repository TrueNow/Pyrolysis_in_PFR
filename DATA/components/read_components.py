import openpyxl
from src.Components import Components


def read_components_from_xlsx(folder: str = './DATA/components',
                              filename: str = 'All_components.xlsx',
                              components_dict: dict = None):
    if components_dict is None:
        components_dict = []
    file = f'{folder}/{filename}'

    xlsx = openpyxl.load_workbook(file, data_only=True)
    sheet = xlsx.active

    components = Components()

    titles = [col[0].value for col in sheet.iter_cols(1, 4)]

    for row in sheet.iter_rows(min_row=2):
        if row[0].value is not None:
            properties = {}
            for col in range(len(titles)):
                properties[titles[col]] = row[col].value
            if properties['name'] in components_dict.keys():
                components.add_component(properties['name'], properties)
    return components
