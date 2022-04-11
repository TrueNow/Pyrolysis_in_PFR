import PySimpleGUI as sg


value = [0, 1, 2, 3]

layout = [
    [
        [
            sg.Tree(data=[['0', '1', '2', '3']], headings=['ID', 'Уравнение', 'A', 'E'],
                    key='Table', justification='left',
                    col_widths=[5, 30], auto_size_columns=False),
            sg.Button('Клик', key='btn')
        ],
    ],
]


window_main = sg.Window('Главное окно', layout=layout)


while True:
    event, values = window_main.read()

    print(event)

    if event == sg.WIN_CLOSED:
        break

    if event == 'btn':
        print(window_main['Table'].get_last_clicked_position())
        pass
