import PySimpleGUI as sg

from src.Reactions import Reactions
from src.Components import Components
from src.Reactor import Cascade
from src.Model import Model

from GUI.winReactions import WinReactions
from GUI.winComponents import WinComposition
from GUI.winReactors import WinReactors
from GUI.winInfo import WinInfo


class WinMain(sg.Window):
    __reactions: dict = {}
    __components: dict = {}
    __cascade: dict = {}
    __all_components: dict = {}

    def __init__(self):
        super(WinMain, self).__init__('Главное окно', layout=self.layout_main())
        self.window_reactions = WinReactions()
        self.window_composition = WinComposition()
        self.window_reactors = WinReactors()
        self.window_info = WinInfo(self)

    def open_main(self):
        while True:
            event, values = self.read()

            if event == sg.WIN_CLOSED:
                break

            if event == '--BUTTON-REACTIONS--':
                self.__reactions, self.__components = self.window_reactions.open()
                self['--TABLE-REACTIONS--'].update(values=self.window_reactions.data)

            elif event == '--BUTTON-COMPONENTS--':
                self.__components = self.window_composition.open(self.__components)
                self['--TABLE-COMPONENTS--'].update(values=self.window_composition.data)

            elif event == '--BUTTON-REACTORS--':
                self.window_reactors.open()
                self['--TABLE-REACTORS--'].update(values=self.window_reactors.data)

            elif event == '--BUTTON-START--':
                self.close()
                reactions = Reactions(self.__reactions)
                components = Components(self.__components)
                cascade = Cascade(self.__cascade)

                Model(reactions=reactions, components=components, cascade=cascade)

                self.window_info.open()

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

    @reactions.setter
    def reactions(self, value: dict):
        self.__reactions = value

    @property
    def components(self):
        return self.__components

    @components.setter
    def components(self, value: dict):
        self.__components = value

    @property
    def cascade(self):
        return self.__cascade

    @cascade.setter
    def cascade(self, value: dict):
        self.__cascade = value

    @property
    def all_components(self):
        return self.__all_components

    @all_components.setter
    def all_components(self, value: dict):
        self.__all_components = value


if __name__ == '__main__':
    window = WinMain()
    window.open_main()
