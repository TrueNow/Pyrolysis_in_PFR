import openpyxl


class Saver:
    """Модуль предназначен для сохранения введенных данных и результатов в таблицу Excel"""

    row_add = 0
    start_col = 0

    def __init__(self, model, name):
        self.model = model
        self.name_file = name

        # Создание Excel файла
        self.xlsx = openpyxl.Workbook()
        sheet = self.xlsx.active
        self.xlsx.remove_sheet(sheet)
        self.xlsx.create_sheet('Результаты')
        self.sheet = self.xlsx['Результаты']

        self.start_row = 0

    def init_in_xlsx(self, number_of_reactor: int):
        number = number_of_reactor  # Порядковый номер реактора начиная с 0
        self.row_add = number * (len(self.model.get_components().get_components()) + 4)
        self.start_col = 0
        value = self.model.get_cascade().get_reactor(number).molar_flow_in
        self.values_in_xlsx(value)

    def result_in_xlsx(self, number_of_reactor: int):
        number = number_of_reactor  # Порядковый номер реактора начиная с 0
        self.row_add = number * (len(self.model.get_components().get_components()) + 4)
        self.start_col = 12
        value = self.model.get_cascade().get_reactor(number).get_section().molar_flow_out
        self.values_in_xlsx(value)

    def values_in_xlsx(self, value: float):
        self.title()

        col_name = self.start_col + 1
        self.name(col_name)

        col_ratio = self.start_col + 2
        self.ratio(col_ratio)

        col_mol_fr = self.start_col + 3
        self.mol_fr(col_mol_fr)

        row = self.start_row + 2 + self.row_add  # 2
        col = self.start_col + 4  # 4
        self.sheet.cell(row=row, column=col).value = value

        col_mol = self.start_col + 4
        self.mol(col_mol)

        col_molar_mass = self.start_col + 5
        self.molar_mass(col_molar_mass)

        col_mass = self.start_col + 6
        self.mass(col_mass)

        col_mass_fr = self.start_col + 7
        self.mass_fr(col_mass_fr)

        self.xlsx.save(f'Result/{self.name_file}')

    def title(self):
        title = {
            self.start_col + 1: 'Components',
            self.start_col + 2: 'Ratio',
            self.start_col + 3: 'MolFr',
            self.start_col + 4: 'Mol',
            self.start_col + 5: 'MolarMass',
            self.start_col + 6: 'Mass',
            self.start_col + 7: 'MassFr'
        }

        row = self.start_row + 1 + self.row_add
        for col in range(1, len(title) + 1):
            self.sheet.cell(row=row, column=self.start_col + col).value = title[self.start_col + col]

    def name(self, col: int):
        row = self.start_row + 3 + self.row_add
        col_name = col
        for name in self.model.get_components().get_components().keys():
            self.sheet.cell(row=row, column=col_name).value = name
            row += 1

    def ratio(self, col: int):
        row = self.start_row + 3 + self.row_add
        col_ratio = col
        for component in self.model.get_components().get_components().values():
            self.sheet.cell(row=row, column=col_ratio).value = component.mol_fr
            self.sheet.cell(row=row, column=col_ratio).number_format = '0.00'
            row += 1
        self.sum_in_column(col_ratio)

    def mol_fr(self, col: int):
        row = self.start_row + 3 + self.row_add
        col_mol_fr = col
        col_ratio = col_mol_fr - 1
        for _ in self.model.get_components().get_components().keys():
            self.sheet.cell(row=row, column=col_mol_fr).value = self.sheet.cell(row=row, column=col_ratio).value
            self.sheet.cell(row=row, column=col_mol_fr).number_format = '0.0000'
            row += 1
        self.sum_in_column(col_mol_fr)

    def mol(self, col: int):
        row = self.start_row + 3 + self.row_add
        col_mol = col
        col_mol_fr = col_mol - 1
        molFlow = self.sheet.cell(row=self.start_row + 2 + self.row_add, column=col_mol).value
        for _ in self.model.get_components().get_components().keys():
            self.sheet.cell(row=row, column=col_mol).value = self.sheet.cell(row=row, column=col_mol_fr).value * molFlow
            self.sheet.cell(row=row, column=col_mol).number_format = '0.00'
            row += 1
        self.sum_in_column(col_mol)

    def molar_mass(self, col: int):
        row = self.start_row + 3 + self.row_add
        col_molar_mass = col
        for component in self.model.get_components().get_components().values():
            self.sheet.cell(row=row, column=col_molar_mass).value = component.molar_mass
            self.sheet.cell(row=row, column=col_molar_mass).number_format = '0.00'
            row += 1

    def mass(self, col: int):
        row = self.start_row + 3 + self.row_add
        col_mass = col
        col_molar_mass = col_mass - 1
        col_mol = col_molar_mass - 1
        for _ in self.model.get_components().get_components().keys():
            molar_mass = self.sheet.cell(row=row, column=col_molar_mass).value
            mol = self.sheet.cell(row=row, column=col_mol).value
            self.sheet.cell(row=row, column=col_mass).value = mol * molar_mass
            self.sheet.cell(row=row, column=col_mass).number_format = '0.00'
            row += 1
        self.sum_in_column(col_mass)

    def mass_fr(self, col: int):
        row = self.start_row + 3 + self.row_add
        col_mass_fr = col
        col_mass = col_mass_fr - 1

        sum_mass = self.sheet.cell(row=self.start_row + 2, column=col_mass).value
        for _ in self.model.get_components().get_components().keys():
            mass = self.sheet.cell(row=row, column=col_mass).value
            self.sheet.cell(row=row, column=col_mass_fr).value = mass / sum_mass
            self.sheet.cell(row=row, column=col_mass_fr).number_format = '0.0000'
            row += 1
        self.sum_in_column(col_mass_fr)

    def sum_in_column(self, col: int):
        row = self.start_row + 3 + self.row_add
        column = col
        s = 0
        for _ in self.model.get_components().get_components().keys():
            s += self.sheet.cell(row=row, column=column).value
            row += 1
        row = self.start_row + 2 + self.row_add
        self.sheet.cell(row=row, column=column).value = s
        self.sheet.cell(row=row, column=column).number_format = '0.00'

    def reactor_in_xlsx(self, i: int):
        parameters = [0, 1,
                      self.model.get_cascade().get_reactor(i).name,
                      self.model.get_cascade().get_reactor(i).temp_in,
                      self.model.get_cascade().get_reactor(i).temp_out,
                      self.model.get_cascade().get_reactor(i).press_in,
                      self.model.get_cascade().get_reactor(i).press_out,
                      self.model.get_cascade().get_reactor(i).volume,
                      self.model.get_cascade().get_reactor(i).steps,
                      self.model.get_cascade().get_reactor(i).get_section().time_count]
        for row in range(2, len(parameters)):
            self.sheet.cell(row=self.start_row + row + self.row_add, column=10).value = parameters[row]
        self.reactor_title()

        self.xlsx.save(f'Result/{self.name_file}')

    def reactor_title(self):
        title = {
            'parameters': [0, 1, 2,
                           'Температура вход', 'Температура выход',
                           'Давление вход', 'Давление выход',
                           'Объем реактора', 'Число секций', 'Время пребывания'],
            'format': [0, 1, 2,
                       '0.0', '0.0',
                       '0.0', '0.0',
                       '0.0', '0', '0.000'],
            'dimension': [0, 1, 2,
                          'C', 'C',
                          'кПа', 'кПа',
                          'м3', 'шт', 'с'],
        }
        for row in range(3, len(title['parameters'])):
            self.sheet.cell(row=self.start_row + row + self.row_add, column=9).value = title['parameters'][row]
            self.sheet.cell(row=self.start_row + row + self.row_add, column=10).number_format = title['format'][row]
            self.sheet.cell(row=self.start_row + row + self.row_add, column=11).value = title['dimension'][row]

    def work(self):
        row_start = 4
        result = self.xlsx.active
        sheet = self.xlsx.create_sheet('Итог')
        for i in range(row_start, int(4 + len(self.model.get_components().get_used_components()))):
            if self.model.get_components().get_component(result.cell(row=i, column=1).value).type == 'mol':
                sheet.cell(row=row_start, column=1).value = result.cell(row=i, column=1).value
                sheet.cell(row=row_start, column=2).value = result.cell(row=i, column=result.max_column - 3).value
                sheet.cell(row=row_start, column=2).number_format = '0.000000'
                sheet.cell(row=row_start, column=3).value = 'мол. доля'
                row_start += 1
        sheet.cell(row=sheet.max_row + 2, column=1).value = 'Расход'
        sheet.cell(row=sheet.max_row, column=2).value = result.cell(row=3, column=result.max_column - 2).value
        sheet.cell(row=sheet.max_row, column=3).value = 'кмоль/с'
