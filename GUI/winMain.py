import PySimpleGUI as sg

from tkinter import messagebox

from src.Model import Model

from GUI.winReactions import WinReactions
from GUI.winComponents import WinComposition
from GUI.winReactors import WinReactors



class WinMain(sg.Window):
    _reactions = ''
    _components = ''
    _cascade = ''

    def __init__(self):
        super(WinMain, self).__init__('Главное окно', layout=self.layout_main(), size=(800, 600))

    def open_main(self):
        while True:
            event, values = self.read()

            if event == sg.WIN_CLOSED:
                break

            if event == 'BUTTON-REACTIONS':
                WinReactions(self).open()

            elif event == 'BUTTON-COMPONENTS':
                WinComposition(self).open()

            elif event == 'BUTTON-REACTORS':
                WinReactors(self).open()

            elif event == 'BUTTON-START':
                self.close()
                Model(reactions=self.reactions, components=self.components, cascade=self.cascade)
                messagebox.showinfo(title='Выполнено', message='Расчет выполнен')

    def update_table(self, window: str, values=None):
        if values is None:
            values = []
        table = f'TABLE-{window}'
        self[table].update(values=values)

    @staticmethod
    def layout_main() -> list:
        layout = [
            [
                [
                    sg.Button(button_text='Реакционный набор', key='BUTTON-REACTIONS', size=(20, 2)),
                    sg.Table(
                        values=[['', '', '', '']], headings=['ID', 'Уравнение', 'A', 'E'],
                        key='TABLE-REACTIONS', justification='left',  size=(20, 2),
                        col_widths=[3, 30, 8, 8], auto_size_columns=False)
                ],
                [
                    sg.Button(button_text='Состав исходного потока', key='BUTTON-COMPONENTS', size=(20, 2)),
                    sg.Table(
                        values=[['', '', '']], headings=['Компонент', 'Мол. доля', 'Масс. доля'],
                        key='TABLE-COMPONENTS', justification='left',
                        size=(20, 2), auto_size_columns=True)
                ],
                [
                    sg.Button(button_text='Выбор реактора', key='BUTTON-REACTORS', size=(20, 2)),
                    sg.Table(
                        values=[[' ', ' ', ' ', ' ', ' ', ' ', ' ']],
                        headings=['Наименование', 'Tвх, C', 'Tвых, C',
                                  'Pвх, кПа', 'Pвых, кПа', 'Объем, м3', 'Секций, шт'],
                        size=(20, 2), key='TABLE-REACTORS', justification='center', auto_size_columns=True)
                ],
                [sg.Button(button_text='Начать', key='BUTTON-START', size=(42, 2))]
            ],
        ]

        return layout

    @property
    def reactions(self):
        return self._reactions

    @reactions.setter
    def reactions(self, value):
        self._reactions = value

    @property
    def components(self):
        return self._components

    @components.setter
    def components(self, value):
        self._components = value

    @property
    def cascade(self):
        return self._cascade

    @cascade.setter
    def cascade(self, value):
        self._cascade = value
