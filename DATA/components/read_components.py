import openpyxl
from src.Components import Components


def read_components_from_xlsx(folder='D:/Models_In_Python/Work_Model v4.0/DATA/components',
                              filename='All_components.xlsx'):
    file = f'{folder}/{filename}'

    xlsx = openpyxl.load_workbook(file, data_only=True)
    sheet = xlsx.active

    components = Components()
    data = []

    titles = [col[0].value for col in sheet.iter_cols(1, 4)]

    for row in sheet.iter_rows(2):
        if row[0].value is not None:
            properties = {}
            for col in range(len(titles)):
                properties[titles[col]] = row[col].value
            components.add_component(properties['name'], properties)
            data.append([*properties.values()])
    return components, data
