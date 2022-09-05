import PySimpleGUI as sg

from src.Flow import Flow, Components, MOL, MASS


class SettingCompositionWindow(sg.Window):
    def __init__(self, components: Components):
        self._flow = Flow(components)
        setting = {'title': 'Состав потока', 'layout': self.layout_composition()}
        super(SettingCompositionWindow, self).__init__(**setting)

    def open(self):
        while True:
            event, values = self.read()

            if event == sg.WIN_CLOSED:
                return False

            elif event == 'OK':
                self.set_composition(values)
                self.close()
                if self._flow.summary_fractions(MOL):
                    return True
                return False

    def set_composition(self, values):
        for component in self._flow.get_composition():
            event = f'INPUT_{component.name}'
            try:
                value = float(values[event])
            except ValueError:
                value = 0

            component.ratio = value
            self._flow.temperature = float(values['temperature'])
            self._flow.pressure = float(values['pressure'])

            try:
                flow = float(values['flow'])
            except ValueError:
                flow = 10

            if values[MOL]:
                self._flow.set_fraction(MOL)
                self._flow.update_composition(value_flow=flow, type_flow=MOL)
            elif values[MASS]:
                self._flow.set_fraction(MASS)
                self._flow.update_composition(value_flow=flow, type_flow=MASS)

    def layout_composition(self) -> list:
        """Оформление окна"""
        setting_input = {
            'enable_events': True,
            'size': (8, 1),
            'justification': 'center'
        }

        column_name, column_input = [], []
        for component in self._flow.get_composition():
            if component.is_molecular():
                column_name.append(
                    [sg.Text(text=f'{component.name}')]
                )
                if component.ratio != 0:
                    default_text = f'{component.ratio}'
                else:
                    default_text = ''
                column_input.append(
                    [
                        sg.Input(
                            key=f'INPUT_{component.name}',
                            default_text=default_text,
                            **setting_input
                        )
                    ]
                )

        column_radio = [
            [sg.Radio(text='Мол. доля', group_id=1,
                      default=True, key=MOL, enable_events=True)],
            [sg.Radio(text='Масс. доля', group_id=1,
                      default=False, key=MASS, enable_events=True)],
            [],
            [sg.Text(text='Расход\nкмоль/с или кг/с')],
            [sg.Input(key='flow', **setting_input)],
            [],
            [sg.Text(text='Давление, кПа')],
            [sg.Input(key='pressure', default_text=300, **setting_input)],
            [],
            [sg.Text(text='Температура, C')],
            [sg.Input(key='temperature', default_text=800, **setting_input)],

        ]

        layout = [
            [
                sg.Column(column_name, vertical_alignment='top'),
                sg.Column(column_input, vertical_alignment='top'),
                sg.VSeperator(),
                sg.Column(column_radio, vertical_alignment='top')
            ],
            [sg.Button('OK', key='OK')]
        ]
        return layout

    def get_flow(self):
        return self._flow

    def data_table_main(self):
        table_data = [
            [
                f'{component.name}',
                f'{component.mol_fraction:.4f}',
                f'{component.mol:2.2f}',
                f'{component.mass:4.2f}',
                f'{component.mass_fraction:.4f}'
            ] for component in self._flow.get_composition()
            if component.is_molecular() and component.mol_fraction
        ]
        table_data.append(
            [
                f'Итого:',
                f'{self._flow.summary_fractions(MOL):.4f}',
                f'{self._flow.summary_flows(MOL):.2f}',
                f'{self._flow.summary_flows(MASS):.2f}',
                f'{self._flow.summary_fractions(MASS):.4f}',
            ]
        )
        return table_data
