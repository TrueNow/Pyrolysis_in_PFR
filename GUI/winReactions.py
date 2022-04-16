import os.path
import PySimpleGUI as sg

from src.Reactions import Reactions
from src.Components import Components
from DATA.reactions.read_reactions import read_reactions_from_xlsx


class WinReactions(sg.Window):
    def __init__(self, main):
        """Инициализация окна определения реакционного набора"""
        super(WinReactions, self).__init__('Реакционный набор')
        self.main = main

    def open(self):
        """Открытие окна и считывание действий"""
        file_list, folder = self.get_files()
        self.layout(self.layout_reactions(file_list))

        while True:
            event, values = self.read()

            if event == sg.WIN_CLOSED:
                break

            if event == 'LIST':
                filename = values[event][0]
                new_reactions = read_reactions_from_xlsx(folder, filename)

                self.main.reactions = Reactions(new_reactions)
                self.main.components = Components(self.main.reactions.choose_used_components())

                for reaction in self.main.reactions.get_reactions().values():
                    reaction.create_equation_reactions(reaction, self.main.components)

                data_table_values = self.update_table()

            elif event == 'OK':
                try:
                    self.main.update_table('REACTIONS', data_table_values)
                except UnboundLocalError:
                    pass
                self.close()

    @staticmethod
    def get_files():
        folder = 'D:/Models_In_Python/Work_Model v4.0/DATA/reactions'
        file_list = os.listdir(folder)
        names = [
            f for f in file_list
            if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith('.xlsx')
        ]
        return names, folder

    # def get_used_components(self) -> dict:
    #     """Сортировка компонентов"""
    #     components_dict = {'Вода': self._dict_all_components['Вода']}
    #     for reaction in self._dict_reactions.values():
    #         for name, coefficient in reaction['Components'].items():
    #             components_dict[name] = self._dict_all_components[name]
    #
    #     sort_components = {}
    #     for component in self._dict_all_components.keys():
    #         if component in components_dict:
    #             sort_components[component] = components_dict[component]
    #     return sort_components

    def update_table(self):
        data_table_values = []
        for id, reaction in self.main.reactions.get_reactions().items():
            data_table_values.append(
                [
                    id,
                    self.main.reactions.get_reaction(id).equation,
                    '{:2.3e}'.format(reaction.A),
                    '{:.2f}'.format(reaction.E)
                ]
            )
        self[f'TABLE'].update(values=data_table_values)
        return data_table_values

    @staticmethod
    def layout_reactions(names) -> list:
        """Оформление окна"""
        column_1 = [
            [
                sg.Listbox(values=names, enable_events=True, size=(20, 10), key='LIST')
            ],
        ]

        column_2 = [
            [
                sg.Table(
                    values=[['', '', '', '']], headings=['ID', 'Уравнение', 'A', 'E'],
                    key='TABLE', justification='left',
                    col_widths=[5, 30], auto_size_columns=False
                )
            ]
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
