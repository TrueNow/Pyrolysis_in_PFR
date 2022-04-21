import openpyxl


class Saver:
    """Модуль предназначен для сохранения введенных данных и результатов в таблицу Excel"""

    start_row = 1

    def __init__(self, model):
        self.model = model
        self.filename = f'{self.model.get_reactions().filename[:-5]} in {self.model.get_cascade().filename[:-5]}.xlsx'

        # Создание Excel файла
        self.xlsx = openpyxl.Workbook()
        self.sheet = self.xlsx.active
        self.sheet.title = 'Результаты'

    def init_in_xlsx(self, start):
        self.start_row = start
        row, column = self.start_row, 1
        self.save_components(row, column)

    def reactor_in_xlsx(self, reactor):
        row, start_column = self.start_row, 8
        list_reactor = [
            [None, reactor.name, None, None, ''],
            ['Температура', reactor.temp_in, reactor.temp_out, 'C', '0.00'],
            ['Давление', reactor.press_in, reactor.press_out, 'кПа', '0.00'],
            ['Объем реактора', reactor.volume, None, 'м3', '0.00'],
            ['Число секций', reactor.steps, None, 'шт', '0'],
            ['Время пребывания', reactor.residence_time, None, 'с', '0.000000']
        ]

        for string in list_reactor:
            column = start_column
            for param in string[:-1]:
                try:
                    self.sheet.cell(row=row, column=column, value=param).number_format = string[-1]
                except:
                    self.sheet.cell(row=row, column=column, value=param)
                column += 1
            row += 1
        self.xlsx.save(f'{self.filename}')

    def result_in_xlsx(self):
        row, column = self.start_row, 13
        self.save_components(row, column)

    def save_components(self, start_row, start_column):
        row = start_row
        column = start_column

        params = self.rounder('Component', 'MolarMass', 'MolFr', 'Mol', 'Mass', 'MassFr')
        for param in params.values():
            self.sheet.cell(row=row, column=column, value=param['value']).number_format = param['rounding']
            column += 1

        for name, component in self.model.get_components().get_components().items():
            row += 1

            column = start_column
            params = self.rounder(name, component.molar_mass, component.mol_fr, component.mol, component.mass, component.mass_fr)
            for param in params.values():
                self.sheet.cell(row=row, column=column, value=param['value']).number_format = param['rounding']
                column += 1

        column = start_column
        row += 1
        components = self.model.get_components()
        params = self.rounder('Сумма', None, components.get_mol_fr(), components.get_mol_flow(), components.get_mass_flow(), components.get_mass_fr())
        for param in params.values():
            self.sheet.cell(row=row, column=column, value=param['value']).number_format = param['rounding']
            column += 1
        self.xlsx.save(f'{self.filename}')

    @staticmethod
    def rounder(one, two, three, four, five, six):
        return {
            '1': {'value': one, 'rounding': ''},
            '2': {'value': two, 'rounding': '0.0000'},
            '3': {'value': three, 'rounding': '0.0000'},
            '4': {'value': four, 'rounding': '0.00'},
            '5': {'value': five, 'rounding': '0.00'},
            '6': {'value': six, 'rounding': '0.0000'},
        }
