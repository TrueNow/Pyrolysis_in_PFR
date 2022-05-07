import PySimpleGUI as sg


class WinComposition(sg.Window):
    def __init__(self, components):
        """Открытие окна определения компонентов потока и считывание действий"""
        super(WinComposition, self).__init__('Состав потока')
        self.components = components
        self.check = False
        self.layout(self.layout_composition())

        while True:
            event, values = self.read()

            match event:
                case sg.WIN_CLOSED:
                    break
                case 'OK':
                    self.check = True
                    self.close()

            match event[:5]:
                case 'INPUT':
                    self.components.get_component(event.split('_')[1]).set_ratio(values[event])
                    self.components.set_mol_fr()
                    self.components.update_properties()
                    data_table = self.components.data_table_components()
                    self['TABLE'].update(values=data_table)

    def layout_composition(self) -> list:
        """Оформление окна"""
        column_input = []
        for name, component in self.components.components.items():
            if component.molecular:
                column_input.append([
                    sg.Input(key=f'INPUT_{name}', enable_events=True, size=(8, 1),
                             justification='center', default_text=f'{component.ratio:.4f}'),
                ])

        values = self.components.data_table_components()

        column_table = [[
            sg.Table(
                values=values,
                headings=['Component', 'Molar. mass', 'Mol. fr', 'Mol', 'Mass', 'Mass. fr'],
                size=(50, 30), font='* 12',
                key='TABLE', justification='center', auto_size_columns=True
            )
        ]]

        layout = [
            [
                sg.Column(column_input, vertical_alignment='top'),
                sg.VSeperator(),
                sg.Column(column_table, vertical_alignment='top')
            ],
            [sg.Button('OK', key='OK')]
        ]

        return layout
