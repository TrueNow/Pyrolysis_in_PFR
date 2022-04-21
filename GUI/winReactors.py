import os.path
import PySimpleGUI as sg
from DATA.reactor.read_reactor import read_reactor_from_xlsx
from src.Reactor import Cascade


class WinReactors(sg.Window):
    folder = 'D:/Models_In_Python/Work_Model v4.0/DATA/reactor'

    def __init__(self, main):
        """Инициализация окна определения каскада реакторов"""
        super(WinReactors, self).__init__('Выбор реактора')
        self.main = main

    def open(self):
        """Открытие окна и считывание действий"""
        file_list, folder = self.get_files()
        self.layout(self.layout_reactor(file_list))

        while True:
            event, values = self.read()

            if event == sg.WIN_CLOSED:
                break

            elif event == 'LIST':
                filename = values[event][0]
                new_cascade = read_reactor_from_xlsx(folder, filename)
                self.main.cascade = Cascade(new_cascade, filename)
                self[f'TABLE'].update(values=self.main.cascade.get_cascade_layout())

            elif event == 'OK':
                try:
                    self.main.update_table('REACTORS', self.main.cascade.get_cascade_layout())
                except UnboundLocalError:
                    pass
                self.close()

    @staticmethod
    def get_files():
        folder = 'D:/Models_In_Python/Work_Model v4.0/DATA/reactor'
        file_list = os.listdir(folder)
        names = [
            f for f in file_list
            if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith('.xlsx')
        ]
        return names, folder

    @staticmethod
    def layout_reactor(filenames) -> list:
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
