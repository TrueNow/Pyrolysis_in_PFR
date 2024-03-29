import os.path
import PySimpleGUI as sg

from DATA.reactions.read_reactions import read_reactions_from_xlsx
from DATA.components.read_components import read_components_from_xlsx

from src.Reactions import Reactions
from src.Flow import Components


class ReactionsWindow(sg.Window):
    _reactions: Reactions
    _components: Components

    def __init__(self):
        """Открытие окна определения реакционного набора и считывание действий"""
        file_list, self.folder = self.get_files()
        setting = {'title': 'Реакционный набор',
                   'layout': self.layout_reactions(file_list)}
        super(ReactionsWindow, self).__init__(**setting)

    def open(self) -> bool:
        while True:
            event, values = self.read()

            if event == sg.WIN_CLOSED:
                return False
            elif event == 'LIST':
                filename = values[event][0]
                self._reactions = read_reactions_from_xlsx(self.folder,
                                                           filename)
                used_components_set = self._reactions.choose_used_components()
                self._components = read_components_from_xlsx(
                    used_components=used_components_set)
                for reaction in self._reactions.get_reactions():
                    reaction.set_equation(self._components)
                self[f'TABLE'].update(values=self.data_table())
            elif event == 'OK':
                self.close()
                return True

    def get_reactions(self):
        return self._reactions

    def get_components(self):
        return self._components

    @staticmethod
    def get_files():
        folder = './DATA/reactions'
        file_list = os.listdir(folder)
        names = [
            f for f in file_list
            if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith(
                '.xlsx')
        ]
        return names, folder

    @staticmethod
    def layout_reactions(names) -> list:
        """Оформление окна"""
        column_1 = [
            [
                sg.Listbox(
                    values=names,
                    enable_events=True,
                    size=(20, 10),
                    key='LIST'
                )
            ],
        ]

        setting_table = {
            'font': '* 12', 'key': 'TABLE',
            'justification': 'center',
            'auto_size_columns': False,
        }
        setting_table_components = {
            'headings': ['ID', 'Уравнение', 'A', 'E'],
            'values': [['', '', '', '']],
            'col_widths': [6, 30, 12, 10],
        }

        column_2 = [
            [sg.Table(**setting_table, **setting_table_components)]
        ]

        layout = [
            [
                sg.Column(column_1),
                sg.VSeperator(),
                sg.Column(column_2)
            ],
            [
                sg.Button('OK', key='OK')
            ],
        ]

        return layout

    def data_table(self) -> list:
        data = []
        for reaction in self._reactions.get_reactions():
            data.append(
                [
                    reaction.id,
                    reaction.equation,
                    f'{reaction.A:2.3e}',
                    f'{reaction.E:.2f}'
                ]
            )
        return data
