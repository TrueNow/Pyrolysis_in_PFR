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
        setting = {'title': 'Реакционный набор', 'layout': self.layout_reactions(file_list)}
        super(ReactionsWindow, self).__init__(**setting)

    def open(self) -> bool:
        while True:
            event, values = self.read()

            if event == sg.WIN_CLOSED:
                return False
            elif event == 'LIST':
                filename = values[event][0]
                self._reactions = read_reactions_from_xlsx(self.folder, filename)
                used_components_set = self._reactions.choose_used_components()
                self._components = read_components_from_xlsx(used_components=used_components_set)
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
            if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith('.xlsx')
        ]
        return names, folder

    @staticmethod
    def layout_reactions(names) -> list:
        """Оформление окна"""
        column_1 = [
            [sg.Listbox(values=names, enable_events=True, size=(20, 10), key='LIST')],
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
            data.append([reaction.id, reaction.equation, f'{reaction.A:2.3e}', f'{reaction.E:.2f}'])
        return data

# class AddReactionsWindow(sg.Window):
#     def __init__(self, main=None):
#         """Открытие окна определения реакционного набора и считывание действий"""
#         super(AddReactionsWindow, self).__init__('Реакционный набор')
#         self.main = main
#         self.layout(self.layout_reactions())
#         self.check = False
#
#     def open(self):
#         while True:
#             event, values = self.read()
#
#             match event:
#                 case sg.WIN_CLOSED:
#                     break
#                 case 'OK':
#                     self.check = True
#                     self.close()
#
#     def layout_reactions(self, list_components=None) -> list:
#         if list_components is None:
#             list_components = ['Этан', 'Этилен', 'Водород']
#         input_size = (10, 1)
#         first_row = [sg.Text(text='ID = ', size=(4, 1)), sg.Input(size=(5, 1)), sg.Combo(list_components), sg.Combo(list_components), sg.Combo(list_components), sg.Combo(list_components), sg.Combo(list_components)],
#         second_row = [sg.Text(text='Стехометрия', size=(10, 1)), sg.Input(size=input_size), sg.Input(size=input_size), sg.Input(size=input_size), sg.Input(size=input_size), sg.Input(size=input_size)]
#         third_row = [sg.Text(text='Порядок', size=(10, 1)), sg.Input(size=input_size), sg.Input(size=input_size), sg.Input(size=input_size), sg.Input(size=input_size), sg.Input(size=input_size)]
#         fourth_row = [sg.Text(text='A, с-1 (м3*кмоль-1*с-1)', size=(20, 1)), sg.Input(size=input_size), sg.Text(text='', size=(8, 1)), sg.Text(text='E, кДж/кмоль', size=(10, 1)), sg.Input(size=input_size)]
#         layout = [
#             first_row, second_row, third_row, fourth_row
#         ]
#         return layout
#
#
# if __name__ == '__main__':
#     window = AddReactionsWindow()
#     window.open()
