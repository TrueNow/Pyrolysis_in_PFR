import openpyxl


def read_components_from_xlsx(folder='D:/Models_In_Python/Work_Model v4.0/DATA/components',
                              filename='All_components.xlsx'):
    """
    components = {
        component: {
            'Молярная масса': float,\n
            'Мольная доля': float,\n
            'Массовая доля': float,\n
            'Тип': str,\n
            'Формула': str\n
        }
    }

    :return: All components from xlsx file
    :rtype: dict
    """

    file = f'{folder}/{filename}'

    xlsx = openpyxl.load_workbook(file, data_only=True)
    sheet = xlsx.active
    components = {}
    row = 2
    while True:
        name = sheet.cell(column=1, row=row).value
        if name is None:
            break
        else:
            components[name] = {}
            for col in range(2, sheet.max_column + 1):
                title_cell = sheet.cell(column=col, row=1)
                value_cell = sheet.cell(column=col, row=row)
                try:
                    components[name][title_cell.value] = float(value_cell.value)
                except TypeError:
                    pass
                except ValueError:
                    components[name][title_cell.value] = value_cell.value
        row += 1
    return components
