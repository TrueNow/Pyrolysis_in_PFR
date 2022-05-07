import os.path
import PySimpleGUI as sg
from DATA.reactor.read_reactor import read_reactor_from_xlsx


class WinReactors(sg.Window):
    def __init__(self):
        """Открытие окна определения каскада реакторов и считывание действий"""
        super(WinReactors, self).__init__('Выбор реактора')
        file_list, folder = self.get_files()
        self.check = True
        self.layout(self.layout_cascade(file_list))

        while True:
            event, values = self.read()

            match event:
                case sg.WIN_CLOSED:
                    self.check = False
                    break
                case 'LIST':
                    filename = values[event][0]
                    self.cascade = read_reactor_from_xlsx(folder=folder, filename=filename)
                    self.data_table = self.cascade.data_table()
                    self[f'TABLE'].update(values=self.data_table)
                case 'OK':
                    self.close()

    def get_cascade(self):
        return self.cascade

    def get_data(self):
        return self.data_table

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
                    values=[['', '', '', '', '']],
                    headings=['Наименование', 'Температура, C', 'Давление, кПа', 'Объем, м3', 'Секций, шт'],
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
