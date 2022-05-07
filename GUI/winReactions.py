import os.path
import PySimpleGUI as sg

from DATA.reactions.read_reactions import read_reactions_from_xlsx
from DATA.components.read_components import read_components_from_xlsx


class WinReactions(sg.Window):
    def __init__(self):
        """Открытие окна определения реакционного набора и считывание действий"""
        super(WinReactions, self).__init__('Реакционный набор')
        file_list, folder = self.get_files()
        self.layout(self.layout_reactions(file_list))
        self.check = False

        while True:
            event, values = self.read()

            match event:
                case sg.WIN_CLOSED:
                    break
                case 'LIST':
                    filename = values[event][0]
                    self.reactions = read_reactions_from_xlsx(folder, filename)
                    components_dict = self.reactions.choose_used_components()
                    self.components = read_components_from_xlsx(components_dict=components_dict)
                    for reaction in self.reactions.reactions.values():
                        reaction.set_equation(self.components)
                    data_table = self.reactions.data_table()
                    self[f'TABLE'].update(values=data_table)
                case 'OK':
                    self.check = True
                    self.close()

    @staticmethod
    def get_files():
        folder = './DATA/reactions'
        file_list = os.listdir(folder)
        names = [
            f for f in file_list
            if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith('.xlsx')
        ]
        return names, folder

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
