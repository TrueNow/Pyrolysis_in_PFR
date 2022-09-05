import os.path
import PySimpleGUI as sg
from DATA.reactor.read_reactor import read_reactor_from_xlsx


class ReactorsWindow(sg.Window):
    def __init__(self):
        """Открытие окна определения каскада реакторов и считывание действий"""
        super(ReactorsWindow, self).__init__('Выбор реактора')
        file_list, folder = self.get_files()
        self.check = False
        self.layout(self.layout_cascade(file_list))

    def open(self):
        while True:
            event, values = self.read()

            if event == sg.WIN_CLOSED:
                return False
            elif event == 'LIST':
                self.cascade = read_reactor_from_xlsx(filename=values[event][0])
                self[f'TABLE'].update(values=self.data_table())
            elif event == 'OK':
                self.close()
                return True

    @staticmethod
    def get_files():
        folder: str = './DATA/reactor'
        file_list = os.listdir(folder)
        names: list = [
            f for f in file_list
            if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith('.xlsx')
        ]
        return names, folder

    def data_table(self) -> list:
        return [[reactor.name, reactor.temperature_string, reactor.pressure_string,
                 reactor.volume, reactor.sections_count] for reactor in self.cascade.get_reactors()]

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
