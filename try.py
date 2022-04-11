import PySimpleGUI as sg
from DATA.components.read_components import read_components_from_xlsx

dict_comps = read_components_from_xlsx()

components = [parameters['Формула'] for parameters in dict_comps.values()]

layout = [
    [
        sg.Text('Компоненты', size=(15, 1), pad=(0, 0), justification='right'),
        sg.Combo(components, size=(8, 5), pad=(0, 0)),
        sg.Text('+', pad=(0, 0)),
        sg.Combo(components, size=(8, 5), pad=(0, 0)),
        sg.Text('--->', pad=(0, 0)),
        sg.Combo(components, size=(8, 5), pad=(0, 0)),
        sg.Text('+', pad=(0, 0)),
        sg.Combo(components, size=(8, 5), pad=(0, 0)),
    ],
    [
        sg.Text('Стехиометрия', size=(15, 1), pad=(0, 0), justification='right'),
        sg.Input(size=(10, 5), pad=(0, 0)),
        sg.Text('  ', pad=(0, 0)),
        sg.Input(size=(10, 5), pad=(0, 0)),
        sg.Text('    ', pad=(0, 0)),
        sg.Input(size=(10, 5), pad=(0, 0)),
        sg.Text('  ', pad=(0, 0)),
        sg.Input(size=(10, 5), pad=(0, 0)),
    ],
    [
        sg.Text('Порядок реакции', size=(15, 1), pad=(0, 0),  justification='right'),
        sg.Input(size=(10, 5), pad=(0, 0)),
        sg.Input(size=(10, 5), pad=(0, 0)),
        sg.Input(size=(10, 5), pad=(0, 0)),
        sg.Input(size=(10, 5), pad=(0, 0)),
    ],
]

win = sg.Window('try', layout=layout)
win.read()