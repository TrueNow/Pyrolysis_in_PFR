import PySimpleGUI as sg

from src.Reactions import Reactions
from src.Components import Components
from src.Reactor import Cascade
from src.Model import Model

from GUI.winReactions import WinReactions
from GUI.winComponents import WinComposition
from GUI.winReactors import WinReactors
from GUI.winInfo import Error


ERROR = Error()


class WinMain(sg.Window):

    global ERROR

    def __init__(self):
        super(WinMain, self).__init__('Главное окно', layout=self.layout_main())
        self.window_reactions = WinReactions()
        self.window_composition = WinComposition()
        self.window_reactors = WinReactors()

        self.__reactions = Reactions()
        self.__components = Components()
        self.__cascade = Cascade()

    def open_main(self):
        while True:
            event, values = self.read()

            if event == sg.WIN_CLOSED:
                break

            if event == '--BUTTON-REACTIONS--':
                self.window_composition.open(self.__components)
                data = self.window_reactions.data

            elif event == '--BUTTON-COMPONENTS--':
                self.window_composition.open(self.__components)
                data = self.window_composition

            elif event == '--BUTTON-REACTORS--':
                self.window_reactors.open()
                self['--TABLE-REACTORS--'].update(values=self.window_reactors.data)

            elif event == '--BUTTON-START--':
                self.close()
                reactions = Reactions(self.__reactions)
                components = Components(self.__components)
                cascade = Cascade(self.__cascade)

                Model(reactions=reactions, components=components, cascade=cascade)

                ERROR.info(title='Выполнено', message='Расчет выполнен')

            try:
                self.update_main(event, data)
            except:
                pass

    def update_main(self, item: str, values=None):
        if values is None:
            values = []
        table = f'--TABLE-{item.split("-")[3]}--'
        self[table].update(values=values)

    @staticmethod
    def layout_main() -> list:
        layout = [
            [
                [
                    sg.Button(button_text='Реакционный набор', key='--BUTTON-REACTIONS--', size=(20, 2)),
                    sg.Table(
                        values=[['', '', '', '']], headings=['ID', 'Уравнение', 'A', 'E'],
                        key='--TABLE-REACTIONS--', justification='left',  size=(20, 2),
                        col_widths=[3, 30, 8, 8], auto_size_columns=False)
                ],
                [
                    sg.Button(button_text='Состав исходного потока', key='--BUTTON-COMPONENTS--', size=(20, 2)),
                    sg.Table(
                        values=[['', '', '']], headings=['Компонент', 'Мол. доля', 'Масс. доля'],
                        key='--TABLE-COMPONENTS--', justification='left',
                        size=(20, 2), auto_size_columns=True)
                ],
                [
                    sg.Button(button_text='Выбор реактора', key='--BUTTON-REACTORS--', size=(20, 2)),
                    sg.Table(
                        values=[[' ', ' ', ' ', ' ', ' ', ' ', ' ']],
                        headings=['Наименование', 'Tвх, C', 'Tвых, C',
                                  'Pвх, кПа', 'Pвых, кПа', 'Объем, м3', 'Секций, шт'],
                        size=(20, 2), key='--TABLE-REACTORS--', justification='center', auto_size_columns=True)
                ],
                [sg.Button(button_text='Начать', key='--BUTTON-START--', size=(42, 2))]
            ],
        ]

        return layout

    @property
    def reactions(self):
        return self.__reactions

    @property
    def components(self):
        return self.__components

    @property
    def cascade(self):
        return self.__cascade
