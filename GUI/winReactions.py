import os.path
import PySimpleGUI as sg
from DATA.reactions.read_reactions import read_reactions_from_xlsx
from DATA.components.read_components import read_components_from_xlsx

folder = 'D:/Models_In_Python/Work_Model v4.0/DATA/reactions'


class WinReactions(sg.Window):
    def __init__(self):
        """Инициализация окна определения реакционного набора"""
        self._dict_all_components = read_components_from_xlsx(filename='All_components.xlsx')
        self._dict_used_components = None
        self._dict_reactions = None

        global folder

        super(WinReactions, self).__init__('Реакционный набор')

    def open(self):
        """Открытие окна и считывание действий"""
        self.layout(self.layout_reactions())
        while True:
            event, values = self.read()

            if event == sg.WIN_CLOSED:
                return self._dict_reactions, self._dict_used_components

            if event == 'List Reactions':
                filename = values['List Reactions'][0]
                self._dict_reactions = read_reactions_from_xlsx(folder, filename)
                self._dict_used_components = self.get_used_components()
                for reaction in self._dict_reactions.values():
                    self.create_equation_reactions(reaction)
                self.show_params_reactions()
                self['OK Reactions'].update(visible=True)

            elif event == 'OK Reactions':
                self.close()
                return self._dict_reactions, self._dict_used_components

    def create_equation_reactions(self, reaction):
        """Создает уравнение одной реакции"""
        inlet, outlet = [], []
        for name, value in reaction['Components'].items():
            if value == -1:
                inlet.append(f"{self._dict_used_components[name]['Формула']}")
            elif value == 1:
                outlet.append(f"{self._dict_used_components[name]['Формула']}")
            elif value < 0:
                inlet.append(f"{-value}{self._dict_used_components[name]['Формула']}")
            elif value > 0:
                outlet.append(f"{value}{self._dict_used_components[name]['Формула']}")
        inlet_str = ' + '.join(inlet)
        outlet_str = ' + '.join(outlet)
        reaction['equation'] = inlet_str + ' ---> ' + outlet_str

    def get_used_components(self) -> dict:
        """Сортировка компонентов"""
        components_dict = {'Вода': self._dict_all_components['Вода']}
        for reaction in self._dict_reactions.values():
            for name, coefficient in reaction['Components'].items():
                components_dict[name] = self._dict_all_components[name]

        sort_components = {}
        for component in self._dict_all_components.keys():
            if component in components_dict:
                sort_components[component] = components_dict[component]
        return sort_components

    def show_params_reactions(self):
        data = []
        for id, reaction in self._dict_reactions.items():
            data.append([id, reaction['equation'], '{:2.3e}'.format(reaction['A']), '{:.2f}'.format(reaction['E'])])
        self['Table Reactions'].update(values=data)
        self.data = data

    @staticmethod
    def layout_reactions() -> list:
        """Оформление окна"""
        file_list = os.listdir(folder)
        names = [
            f for f in file_list
            if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith('.xlsx')
        ]

        column_1 = [
            [
                sg.Listbox(values=names, enable_events=True, size=(20, 10), key='List Reactions')
            ],
        ]

        column_2 = [
            [
                sg.Table(
                    values=[['', '', '', '']], headings=['ID', 'Уравнение', 'A', 'E'],
                    key='Table Reactions', justification='left',
                    col_widths=[5, 30], auto_size_columns=False
                )
            ]
        ]

        layout = [
            [
                sg.Column(column_1),
                sg.VSeperator(),
                sg.Column(column_2)
            ],
            [
                sg.Button('OK', key='OK Reactions', visible=False)
            ],
        ]

        return layout
