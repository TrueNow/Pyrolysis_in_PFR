import PySimpleGUI as sg

from src.Model import Model

from GUI.reactionsWindow import ReactionsWindow
from GUI.componentsWindow import SettingCompositionWindow
from GUI.reactorsWindow import ReactorsWindow

from src.Reactions import Reactions
from src.Flow import Flow, Components
from src.Reactor import Cascade

from datetime import datetime


class MainWindow(sg.Window):
    _reactions: Reactions
    _components: Components
    _flow: Flow
    _cascade: Cascade

    def __init__(self):
        sg.theme("Dark")
        settings = {'title': 'Главное окно', 'layout': self.layout_main()}
        super(MainWindow, self).__init__(**settings)

    def open(self):
        while True:
            event, values = self.read()

            match event:
                case sg.WIN_CLOSED:
                    break
                case "BUTTON-REACTIONS":
                    self.win_reactions()
                case "BUTTON-COMPONENTS":
                    self.win_components()
                case "BUTTON-REACTORS":
                    self.win_reactor()
                case "BUTTON-START":
                    self.start()

    def win_reactions(self):
        win_reactions = ReactionsWindow()
        check = win_reactions.open()
        if check:
            self._reactions = win_reactions.get_reactions()
            self._components = win_reactions.get_components()
            self["TABLE-REACTIONS"].update(values=win_reactions.data_table())

    def win_components(self):
        # try:
        win_components = SettingCompositionWindow(self._components)
        check = win_components.open()
        if check:
            self._flow = win_components.get_flow()
            self["TABLE-COMPONENTS"].update(win_components.data_table_main())
        # except AttributeError:
        #     messagebox.showerror(title='Ошибка', message='Выберите реакционный набор')
        #     self.win_reactions()

    def win_reactor(self):
        win_reactors = ReactorsWindow()
        check = win_reactors.open()
        if check:
            self._cascade = win_reactors.cascade
            self["TABLE-REACTORS"].update(win_reactors.data_table())

    def start(self):
        # try:
        #     a = bool(self._components.summary_parameter('mol_fraction'))
        # except AttributeError:
        #     a = False
        # b = isinstance(self._reactions, Reactions)
        # c = isinstance(self._cascade, Cascade)
        # if all([a, b, c]):
        #     print('Yeah!')
        # else:
        #     error_text = ['Не задан состав потока', 'Не выбран реакционный набор', 'Не выбран реактор']
        #     messagebox.showerror(title='Выполнено', message=error_text[[b, c].index(False)])
        # if self._flow.summary_fractions('mol'):
        #     if isinstance(self._reactions, Reactions):
        #         if isinstance(self._cascade, Cascade):
        #             self.close()
        START = datetime.now()
        self.close()
        model = Model(reactions=self._reactions, flow=self._flow, cascade=self._cascade)
        model.calculate()
        print(datetime.now() - START)
        #             messagebox.showinfo(title='Выполнено', message='Расчет выполнен')
        #         else:
        #             messagebox.showerror(title='Ошибка', message='Не выбран реактор')
        #     else:
        #         messagebox.showerror(title='Ошибка', message='Не выбран реакционный набор')
        # else:
        #     messagebox.showerror(title='Ошибка', message='Не выбран состав потока')

    @staticmethod
    def layout_main() -> list:
        button_size = (15, 5)
        button_pad = (10, 10)
        table_size = (20, 5)
        table_pad = (10, 5)

        setting_button = {
            'size': button_size,
            'pad': button_pad
        }

        setting_table = {
            'pad': table_pad,
            'justification': 'center',
            'size': table_size,
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
            'headings': ['Наименование', 'Температура, C', 'Давление, кПа', 'Объем, м3', 'Секций, шт'],
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
            [sg.Button(button_text='Реакционный\nнабор', key='BUTTON-REACTIONS', **setting_button)],
            [sg.Button(button_text='Состав\nисходного\nпотока', key='BUTTON-COMPONENTS', **setting_button)],
            [sg.Button(button_text='Выбор\nреактора', key='BUTTON-REACTORS', **setting_button)]
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
