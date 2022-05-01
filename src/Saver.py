import openpyxl


class Saver:
    """Модуль предназначен для сохранения введенных данных и результатов в таблицу Excel"""

    _ROW = 1
    _NEXT_ROW = 5
    _INIT_COMPONENTS_COLUMN = 1
    _REACTOR_COLUMN = 8
    _RESULT_COMPONENTS_COLUMN = 14

    def __init__(self, model):
        self.model = model
        self.filename = f'{self.model.get_reactions().filename[:-5]} in {self.model.get_cascade().filename[:-5]}.xlsx'

        # Создание Excel файла
        self.xlsx = openpyxl.Workbook()
        self.sheet = self.xlsx.active
        self.sheet.title = 'Результаты'

    def init_in_xlsx(self):
        row, column = self._ROW, self._INIT_COMPONENTS_COLUMN
        self.save_components(row, column)

    def reactor_in_xlsx(self, reactor):
        PARAMETERS = [
            [reactor.name, 'Вход', 'Выход', None],
            ['Температура', reactor.temperature_inlet, reactor.temperature_outlet, 'C'],
            ['Давление', reactor.pressure_inlet, reactor.pressure_outlet, 'кПа'],
            ['Объем реактора', reactor.volume, None, 'м3'],
            ['Число секций', reactor.number_of_sections, None, 'шт'],
            ['Время пребывания', reactor.time, None, 'с']
        ]
        ROUNDING = ['', '0.00', '0.00', '0.00', '0', '0.000000']

        row, column = self._ROW, self._REACTOR_COLUMN
        for current_row in range(len(PARAMETERS)):
            for current_column in range(len(PARAMETERS[current_row])):
                cell = self.sheet.cell(row=row + current_row, column=column + current_column)
                cell.value = PARAMETERS[current_row][current_column]
                cell.number_format = ROUNDING[current_row]

        self.xlsx.save(f'{self.filename}')

    def result_in_xlsx(self):
        row, column = self._ROW, self._RESULT_COMPONENTS_COLUMN
        self.save_components(row, column)
        self._ROW += (self._NEXT_ROW + len(self.model.get_components().components))

    def save_components(self, start_row, start_column):
        row = start_row
        column = start_column

        components = self.model.get_components()

        TITLES = ['Component', 'MolarMass', 'MolFr', 'Mol', 'Mass', 'MassFr']
        COMPONENTS = {}
        for name, component in components.components.items():
            if component.type:
                COMPONENTS[name] = [component.name, component.molar_mass, component.mol_fraction,
                                    component.mol, component.mass, component.mass_fraction]
        RESULT = ['Сумма', None, components.summary_mol_fraction(), components.summary_mol_flow(),
                  components.summary_mass_flow(), components.summary_mass_fraction()]
        ROUNDING = ['', '0.00', '0.0000', '0.00', '0.00', '0.0000']

        for current_column in range(len(TITLES)):
            cell = self.sheet.cell(row=row, column=column + current_column)
            cell.value = TITLES[current_column]
            cell.number_format = ROUNDING[current_column]
        row += 1

        for name, properties in COMPONENTS.items():
            for current_column in range(len(properties)):
                cell = self.sheet.cell(row=row, column=column + current_column)
                cell.value = properties[current_column]
                cell.number_format = ROUNDING[current_column]
            row += 1

        for current_column in range(len(RESULT)):
            cell = self.sheet.cell(row=row, column=column + current_column)
            cell.value = RESULT[current_column]
            cell.number_format = ROUNDING[current_column]

        self.xlsx.save(f'{self.filename}')
