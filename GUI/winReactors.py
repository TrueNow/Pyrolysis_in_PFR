import os.path
import PySimpleGUI as sg
from DATA.reactor.read_reactor import read_reactor_from_xlsx


folder = 'D:/Models_In_Python/Work_Model v4.0/DATA/reactor'


class WinReactors(sg.Window):
    def __init__(self):
        super(WinReactors, self).__init__('Выбор реактора', self.layout_reactor())

        global folder

    def open(self):
        while True:
            event, values = self.read()

            if event == sg.WIN_CLOSED:
                return self.cascade

            elif event == 'List Reactor':
                filename = values['List Reactor'][0]
                self.cascade = read_reactor_from_xlsx(folder, filename)
                self.show_params_reactor()
                self['OK Reactor'].update(visible=True)

            elif event == 'OK Reactor':
                self.close()
                return self.cascade

    def show_params_reactor(self):
        values = []
        for number, reactor in self.cascade.items():
            data = []
            for key, value in reactor.items():
                data.append(value)
            values.append(data)
        self['Table Reactor'].update(values=values)
        self.data = values

    @staticmethod
    def layout_reactor() -> list:
        file_list = os.listdir(folder)
        filenames = [
            f for f in file_list
            if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith('.xlsx')
        ]

        reactor_1 = [
            [sg.Listbox(values=filenames, enable_events=True, size=(20, 10), key='List Reactor')],
        ]

        reactor_2 = [
            [
                sg.Table(
                    values=[[' ', ' ', ' ', ' ', ' ', ' ', ' ']],
                    headings=['Наименование', 'Tвх, C', 'Tвых, C',
                              'Pвх, кПа', 'Pвых, кПа', 'Объем, м3', 'Секций, шт'],
                    size=(50, 10), font='* 12',
                    key='Table Reactor', justification='center', auto_size_columns=True
                )
            ]
        ]

        reactor = [
            [
                sg.Column(reactor_1, key='Column Reactor Inlet'),
                sg.VSeperator(),
                sg.Column(reactor_2, key='Column Reactor Text')
            ],
            [
                sg.Button('OK', key='OK Reactor')
            ]
        ]
        return reactor
