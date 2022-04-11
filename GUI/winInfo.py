import PySimpleGUI as sg


class WinInfo:
    def __init__(self, main):
        self.__main = main

    def open(self):
        window_info = sg.Window('Выполнено',
                                layout=[
                                    [sg.Text('Расчет завершен')],
                                    [sg.Button('Закрыть', key='--INFO--')]
                                ],
                                background_color='WHITE')

        while True:
            event, values = window_info.read()

            if event == sg.WIN_CLOSED:
                break

            if event == '--INFO--':
                window_info.close()
                break