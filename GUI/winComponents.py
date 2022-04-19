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
        global data_table_values
        if self.main.components == '':
            components = read_components_from_xlsx()
            self.main.components = Components(components)
        self.layout(self.layout_composition())

        while True:
            event, values = self.read()

            if event == sg.WIN_CLOSED:
                break

            elif event.split('_')[0] == 'INPUT':
                self.main.components.get_component(event.split('_')[1]).mol_fr = values[event]
                self.main.components.calculate_fractions(values)
                data_table_values = self.update_data()

            elif event == 'OK':
                try:
                    self.main.update_table('COMPONENTS', data_table_values)
                    print(data_table_values)
                except UnboundLocalError:
                    pass
                self.close()

    def update_data(self):
        table_data = []
        for name, component in self.main.components.get_components().items():
            mol = f'{component.mol_fr:.4f}'
            mass = f'{component.mass_fr:.4f}'
            if component.type:
                self[f'MOL_{name}'].update(mol)
                self[f'MASS_{name}'].update(mass)
                table_data.append([name, mol, mass])
        return table_data

    def layout_composition(self) -> list:
        """Оформление окна"""
        column_input = [[
            sg.Text(text="Компонент", size=(12, 1), justification='center'),
            sg.Text(text="Мол. доля", size=(8, 1), justification='center'),
            sg.Text(text="Молярная масса", size=(14, 1), justification='center'),
            sg.Text(text="Мол. доля", size=(10, 1), justification='center'),
            sg.Text(text="Масс. доля", size=(10, 1), justification='center'),
        ]]

        for name, component in self.main.components.get_components().items():
            if component.type:
                column_input.append([
                    sg.Text(text=f'{name}', size=(12, 1), justification='center'),
                    sg.Input(key=f'INPUT_{name}', enable_events=True, size=(10, 1), justification='center', default_text=f'{component.mol_fr:.4f}'),
                    sg.Text(text=f'{component.molar_mass:.4f}', key=f'MOLMASS_{name}', size=(14, 1), justification='center'),
                    sg.Text(text=f'{component.mol_fr:.4f}', key=f'MOL_{name}', size=(10, 1), justification='center'),
                    sg.Text(text=f'{component.mass_fr:.4f}', key=f'MASS_{name}', size=(10, 1), justification='center'),
                ])

        layout = [
            [sg.Column(column_input, vertical_alignment='top')],
            [sg.Button('OK', key='OK')]
        ]

        return layout
