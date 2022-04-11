import PySimpleGUI as sg
from DATA.components.read_components import read_components_from_xlsx

folder = 'D:/Models_In_Python/Work_Model v4.0/DATA/components'


class WinComposition(sg.Window):
    def __init__(self):
        """Инициализация окна определения компонентов потока"""
        self._dict_all_components = read_components_from_xlsx(filename='All_components.xlsx')
        self._dict_used_components = None
        super(WinComposition, self).__init__('Состав потока')

    def open(self, components):
        """Открытие окна и считывание действий"""
        self._dict_used_components = components
        if len(self._dict_used_components) == 0:
            self.layout(self.layout_composition(self._dict_all_components))
        else:
            self.layout(self.layout_composition(self._dict_used_components))

        while True:
            event, values = self.read()

            if event == sg.WIN_CLOSED:
                return self._dict_used_components

            elif event == 'OK Components':
                try:
                    self.save_fractions()
                except UnboundLocalError:
                    pass
                self.close()
                return self._dict_used_components

            elif event[:2] == 'In':
                self.calculate_fractions(values)

    def calculate_fractions(self, values):
        """Расчет компонентоного состава"""
        values_table = self['Table Components'].get()
        print(values_table)

        name = 0
        mol_mass = 1
        mol = 2
        mass = 3

        lst_components = []
        for in_component in values.keys():
            lst = in_component.split(' ')
            if lst[0] == 'In':
                lst_components.append(lst[-1])

        for component in lst_components:
            i = lst_components.index(component)
            try:
                values_table[i][mol] = float(values[f'In {component}'])
            except ValueError:
                values_table[i][mol] = 0

        summary_mol = 0
        for value in values_table:
            summary_mol += value[mol]

        for component in lst_components:
            i = lst_components.index(component)
            value_mol = values_table[i][mol]
            try:
                values_table[i][mol] = value_mol / summary_mol
            except ZeroDivisionError:
                values_table[i][mol] = 0
            values_table[i][mass] = value_mol * float(values_table[i][mol_mass])

        summary_mass = 0
        for value in values_table:
            summary_mass += value[mass]

        for component in lst_components:
            i = lst_components.index(component)
            value_mass = values_table[i][mass]
            try:
                values_table[i][mass] = float(value_mass / summary_mass)
            except ZeroDivisionError:
                values_table[i][mass] = 0

        self['Table Components'].update(values_table)
        self.data = values_table

    def save_fractions(self):
        """Сохранение состава"""
        name = 0
        mol = 2
        mass = 3

        for row in self.data:
            if row[mol] > 0:
                self._dict_used_components[row[name]] = self._dict_all_components[row[name]]
                self._dict_used_components[row[name]]['Мольная доля'] = row[mol]
                self._dict_used_components[row[name]]['Массовая доля'] = row[mass]

    @staticmethod
    def layout_composition(components) -> list:
        """Оформелние окна"""
        column_input = []
        table = []

        for comp, params in components.items():
            if params['Тип'] == 'mol':
                column_input.append([sg.In(key=f'In {comp}', enable_events=True)])
                table.append([comp, "{:.4f}".format(params['Молярная масса']), 0, 0])

        layout = [
            [
                sg.Column(column_input, vertical_alignment='top'),
                sg.Table(
                    values=table,
                    headings=['Название', 'Моляр. масса, г/моль', 'Мол. доля', 'Масс. доля'],
                    justification='center', auto_size_columns=True, size=(30, 30),
                    key='Table Components', bind_return_key=True
                )
            ],
            [
                sg.Button('OK', key='OK Components')
            ]
        ]

        return layout
