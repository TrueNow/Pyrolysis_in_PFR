import PySimpleGUI as sg

from GUI.componentsWindow import SettingCompositionWindow
from GUI.reactionsWindow import ReactionsWindow
from GUI.reactorsWindow import ReactorsWindow
from src.Flow import Flow, Components
from src.Reactions import Reactions
from src.Reactor import Cascade

from src.Model import Model


class MainWindow(sg.Window):
    _components: Components
    _cascade: Cascade
    _flow: Flow
    _reactions: Reactions

    def __init__(self):
        sg.theme('dark')
        settings = {'title': 'Главное окно', 'layout': self.layout_main()}
        super(MainWindow, self).__init__(**settings)

    def open(self):
        while True:
            event, values = self.read()

            if event == sg.WIN_CLOSED:
                break
            elif event == 'BUTTON-REACTIONS':
                self.win_reactions()
            elif event == 'BUTTON-COMPONENTS':
                self.win_components()
            elif event == 'BUTTON-REACTORS':
                self.win_reactor()
            elif event == 'BUTTON-START':
                self.start()

    def win_reactions(self):
        win_reactions = ReactionsWindow()
        check = win_reactions.open()
        if check:
            self._reactions = win_reactions.get_reactions()
            self._components = win_reactions.get_components()
            self['TABLE-REACTIONS'].update(values=win_reactions.data_table())

    def win_components(self):
        win_components = SettingCompositionWindow(self._components)
        check = win_components.open()
        if check:
            self._flow = win_components.get_flow()
            self['TABLE-COMPONENTS'].update(win_components.data_table_main())

    def win_reactor(self):
        win_reactors = ReactorsWindow()
        check = win_reactors.open()
        if check:
            self._cascade = win_reactors.cascade
            self['TABLE-REACTORS'].update(win_reactors.data_table())

    def start(self):
        self.close()
        model = Model(reactions=self._reactions, flow=self._flow, cascade=self._cascade)
        model.calculate()

    @staticmethod
    def layout_main() -> list:
        BTN_SIZE = (15, 5)
        BTN_PAD = (10, 10)
        TABLE_SIZE = (20, 5)
        TABLE_PAD = (10, 5)

        setting_button = {
            'size': BTN_SIZE,
            'pad': BTN_PAD
        }

        setting_table = {
            'pad': TABLE_PAD,
            'justification': 'center',
            'size': TABLE_SIZE,
            'auto_size_columns': False,
        }

        setting_table_reactions = {
            'values': [['', '', '', '']],
            'headings': ['ID', 'Уравнение', 'A', 'E'],
            'key': 'TABLE-REACTIONS',
            'col_widths': [7, 30, 10, 10],
        }

        setting_table_components = {
            'values': [['', '', '', '', '']],
            'headings': ['Компонент', 'Мол. доля', 'Моль', 'кг', 'Масс. доля'],
            'key': 'TABLE-COMPONENTS',
            'col_widths': [20, 8, 8, 13, 8],
        }

        setting_table_reactors = {
            'values': [['', '', '', '', '']],
            'headings': [
                'Наименование', 'Температура, C',
                'Давление, кПа', 'Объем, м3', 'Секций, шт'
            ],
            'key': 'TABLE-REACTORS',
            'col_widths': [15, 11, 11, 10, 10],
        }

        setting_button_start = {
            'button_text': 'Начать',
            'key': 'BUTTON-START',
            'size': (30, 2),
            'button_color': 'Green',
            'font': 'Arial 20 bold',
            'bind_return_key': True
        }

        column1 = [
            [
                sg.Button(
                    button_text='Реакционный\nнабор',
                    key='BUTTON-REACTIONS',
                    **setting_button
                )
            ],
            [
                sg.Button(
                    button_text='Состав\nисходного\nпотока',
                    key='BUTTON-COMPONENTS',
                    **setting_button
                )
            ],
            [
                sg.Button(
                    button_text='Выбор\nреактора',
                    key='BUTTON-REACTORS',
                    **setting_button
                )
            ]
        ]

        column2 = [
            [sg.Table(**setting_table_reactions, **setting_table)],
            [sg.Table(**setting_table_components, **setting_table)],
            [sg.Table(**setting_table_reactors, **setting_table)],
        ]

        layout = [
            [
                sg.Column(column1, vertical_alignment='top'),
                sg.VSeperator(),
                sg.Column(column2, vertical_alignment='top')
            ],
            [
                sg.Button(**setting_button_start)
            ]
        ]

        return layout
