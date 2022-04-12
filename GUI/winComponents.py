import PySimpleGUI as sg
from src.Components import Components


class WinComposition(sg.Window):
    components: Components

    def __init__(self):
        """Инициализация окна определения компонентов потока"""
        super(WinComposition, self).__init__('Состав потока')

    def open(self, components):
        """Открытие окна и считывание действий"""
        self.components = components

        self.layout(self.layout_composition())

        while True:
            event, values = self.read()

            if event == sg.WIN_CLOSED:
                break

            elif event == 'OK Components':
                self.close()

            elif event[:5] == 'INPUT':
                self.calculate_fractions()
                self.update_data()

    def calculate_fractions(self):
        """Расчет компонентоного состава"""
        summary_mol = 0
        summary_mass = 0
        for name, component in self.components.get_components().items():
            if component.type:
                try:
                    component.mol_fr = float(self[f'INPUT_{name}'].get())
                except ValueError:
                    component.mol_fr = 0
                component.mass_fr = component.mol_fr * component.molar_mass
            summary_mol += component.mol_fr
            summary_mass += component.mass_fr

        for component in self.components.get_components().values():
            try:
                component.mol_fr /= summary_mol
                component.mass_fr /= summary_mass
            except ZeroDivisionError:
                component.mol_fr = 0
                component.mass_fr = 0

    def update_data(self):
        for name, component in self.components.get_components().items():
            if component.type:
                self[f'MOL_{name}'].update('{:.4f}'.format(component.mol_fr))
                self[f'MASS_{name}'].update('{:.4f}'.format(component.mass_fr))

    def layout_composition(self) -> list:
        """Оформление окна"""
        column_input = []

        column_input.append(
            [
                sg.Text(text="Компонент", size=(12, 1), justification='center'),
                sg.Text(text="Мол. доля", size=(8, 1), justification='center'),
                sg.Text(text="Молярная масса", size=(14, 1), justification='center'),
                sg.Text(text="Мол. доля", size=(10, 1), justification='center'),
                sg.Text(text="Масс. доля", size=(10, 1), justification='center'),
            ]
        )

        for name, component in self.components.get_components().items():
            if component.type:
                column_input.append(
                    [
                        sg.Text(text="{}".format(name), size=(12, 1), justification='center'),
                        sg.Input(key=f'INPUT_{name}', enable_events=True, size=(10, 1), justification='center'),
                        sg.Text(text="{:.4f}".format(component.molar_mass), key=f'MOLMASS_{name}', size=(14, 1), justification='center'),
                        sg.Text(text="{:.4f}".format(component.mol_fr), key=f'MOL_{name}', size=(10, 1), justification='center'),
                        sg.Text(text="{:.4f}".format(component.mass_fr), key=f'MASS_{name}', size=(10, 1), justification='center'),
                    ]
                )

        layout = [
            [
                sg.Column(column_input, vertical_alignment='top')
            ],
            [
                sg.Button('OK', key='OK Components')
            ]
        ]

        return layout
