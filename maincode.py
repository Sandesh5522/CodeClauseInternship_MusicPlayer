import PySimpleGUI as sg
# import pygame as pg
import os

sg.theme('DarkAmber')

layout = [
    [sg.Text('Python Music Player!!')],
    [sg.Image(), sg.FolderBrowse('FolderBrowse')],
    [sg.Multiline(key = 'folder', size = (40,40), auto_refresh = True, auto_size_text = True, autoscroll = True)],
    [sg.Submit(), sg.Button('Cancel')]
]

window = sg.Window('Python Music Player', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    elif event == 'Submit':
        foldername = values['FolderBrowse'] or '.'
        filenames = os.listdir(foldername)
        window['folder'].update("\n".join(filenames))
        # print('ok')

print("https://github.com/PySimpleGUI/PySimpleGUI/issues/4393#issuecomment-859296723")
print("https://stackoverflow.com/questions/63725995/how-to-display-files-in-folder-when-using-pysimplegui-filebrowse-function")

window.close()
