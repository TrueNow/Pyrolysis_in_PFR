import PySimpleGUI as sg

from src.Components import Components
from DATA.components.read_components import read_components_from_xlsx


class WinComposition(sg.Window):

    def __init__(self, main):
        """Инициализация окна определения компонентов потока"""
        super(WinComposition, self).__init__('Состав потока')
        self.main = main

    def open(self):
        """Открытие окна и считывание действий"""
        if self.main.components == '':
            components = read_components_from_xlsx()
            self.main.components = Components(components)
        self.layout(self.layout_composition())

        while True:
            event, values = self.read()

            if event == sg.WIN_CLOSED:
                break

            elif event.split('_')[0] == 'INPUT':
                self.main.components.get_component(event.split('_')[1]).ratio = values[event]
                self.main.components.calculate_components()
                data_table_values = self.update_data()
                self[f'TABLE'].update(values=data_table_values)

            elif event == 'OK':
                try:
                    self.main.update_table('COMPONENTS', data_table_values)
                except UnboundLocalError:
                    pass
                self.close()

    def update_data(self):
        table_data = []
        for name, component in self.main.components.get_components().items():
            if component.type:
                table_data.append([
                    name,
                    f'{component.ratio:.4f}',
                    f'{component.molar_mass:.2f}',
                    f'{component.mol_fr:.4f}',
                    f'{component.mol:.2f}',
                    f'{component.mass:.2f}',
                    f'{component.mass_fr:.4f}',
                ])
        return table_data

    def layout_composition(self) -> list:
        """Оформление окна"""
        column_input = []
        for name, component in self.main.components.get_components().items():
            column_input.append([
                sg.Input(key=f'INPUT_{name}', enable_events=True, size=(10, 1),
                         justification='center', default_text=f'{component.ratio:.4f}'),
            ])

        values = self.update_data()

        column_table = [[
            sg.Table(
                values=values,
                headings=['Component', 'Ratio', 'Molar. mass', 'Mol. fr', 'Mol', 'Mass', 'Mass. fr'],
                size=(50, 30), font='* 12',
                key='TABLE', justification='center', auto_size_columns=True
            )
        ]]

        layout = [
            [sg.Column(column_input, vertical_alignment='top'), sg.VSeperator(), sg.Column(column_table, vertical_alignment='top')],
            [sg.Button('OK', key='OK')]
        ]

        return layout
