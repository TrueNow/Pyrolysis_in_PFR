import os.path
import PySimpleGUI as sg
from DATA.reactor.read_reactor import read_reactor_from_xlsx


class WinReactors(sg.Window):
    folder = './DATA/reactor'

    def __init__(self, main):
        """Инициализация окна определения каскада реакторов"""
        super(WinReactors, self).__init__('Выбор реактора')
        self.main = main

    def open(self):
        """Открытие окна и считывание действий"""
        file_list, folder = self.get_files()
        self.layout(self.layout_cascade(file_list))

        while True:
            event, values = self.read()

            if event == sg.WIN_CLOSED:
                break

            elif event == 'LIST':
                filename = values[event][0]
                cascade, cascade_table = read_reactor_from_xlsx(folder, filename)
                self[f'TABLE'].update(values=cascade_table)

            elif event == 'OK':
                try:
                    self.main.cascade, cascade_table = cascade, cascade_table
                    self.main[f'TABLE-REACTORS'].update(cascade_table)
                except UnboundLocalError:
                    pass
                self.close()

    @staticmethod
    def get_files():
        folder: str = './DATA/reactor'
        file_list = os.listdir(folder)
        names: list = [
            f for f in file_list
            if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith('.xlsx')
        ]
        return names, folder

    @staticmethod
    def layout_cascade(filenames) -> list:
        reactor_1 = [
            [sg.Listbox(values=filenames, enable_events=True, size=(20, 10), key='LIST')],
        ]

        reactor_2 = [
            [
                sg.Table(
                    values=[['', '', '', '', '', '', '']],
                    headings=['Наименование', 'Tвх, C', 'Tвых, C', 'Pвх, кПа', 'Pвых, кПа', 'Объем, м3', 'Секций, шт'],
                    size=(50, 10), font='* 12',
                    key='TABLE', justification='center', auto_size_columns=True
                )
            ]
        ]

        reactor = [
            [
                sg.Column(reactor_1),
                sg.VSeperator(),
                sg.Column(reactor_2)
            ],
            [
                sg.Button('OK', key='OK')
            ]
        ]
        return reactor
