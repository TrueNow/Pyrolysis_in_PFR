import PySimpleGUI as sg

from tkinter import messagebox

from src.Model import Model

from GUI.winReactions import WinReactions
from GUI.winComponents import WinComposition
from GUI.winReactors import WinReactors

from src.Reactions import Reactions
from src.Components import Components
from src.Reactor import Cascade


class WinMain(sg.Window):
    _reactions = ''
    _components = ''
    _cascade = ''

    def __init__(self):
        super(WinMain, self).__init__('Главное окно', layout=self.layout_main(), size=(800, 600))

    def open_main(self):
        while True:
            event, values = self.read()

            match event:
                case sg.WIN_CLOSED:
                    break
                case "BUTTON-REACTIONS":
                    self.win_reactions()
                case "BUTTON-COMPONENTS":
                    self.win_components()
                case "BUTTON-REACTORS":
                    self.win_reactor()
                case "BUTTON-START":
                    self.start()

    def win_reactions(self):
        win_reactions = WinReactions()
        if win_reactions.check:
            self._reactions = win_reactions.reactions
            self._components = win_reactions.components
            self["TABLE-REACTIONS"].update(self._reactions.data_table())

    def win_components(self):
        try:
            win_components = WinComposition(self._components)
            if win_components.check:
                self._components = win_components.components
                self["TABLE-COMPONENTS"].update(self._components.data_table_main())
        except AttributeError:
            messagebox.showerror(title='Ошибка', message='Выберите реакционный набор')
            self.win_reactions()

    def win_reactor(self):
        win_reactors = WinReactors()
        if win_reactors.check:
            self._cascade = win_reactors.cascade
            self["TABLE-REACTORS"].update(self._cascade.data_table())

    def start(self):
        if self._components.summary_mol_fraction():
            if isinstance(self._reactions, Reactions):
                if isinstance(self._cascade, Cascade):
                    self.close()
                    Model(reactions=self._reactions, components=self._components, cascade=self._cascade)
                    messagebox.showinfo(title='Выполнено', message='Расчет выполнен')
                else:
                    messagebox.showerror(title='Ошибка', message='Не выбран реактор')
            else:
                messagebox.showerror(title='Ошибка', message='Не выбран реакционный набор')
        else:
            messagebox.showerror(title='Ошибка', message='Не выбран состав потока')

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
                        values=[['', '', '', '', '']],
                        headings=['Наименование', 'Температура, C', 'Давление, кПа', 'Объем, м3', 'Секций, шт'],
                        size=(20, 2), key='TABLE-REACTORS', justification='center', auto_size_columns=True)
                ],
                [sg.Button(button_text='Начать', key='BUTTON-START', size=(42, 2))]
            ],
        ]

        return layout
