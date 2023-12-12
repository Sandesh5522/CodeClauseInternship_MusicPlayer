import PySimpleGUI as sg
import pygame as pg
import os

sg.theme('DarkAmber')

filenames = []

layout = [
    [sg.Text('Python Music Player!!', justification='center', size=(100,1))],
    [sg.FolderBrowse(key = 'FolderBrowse'), sg.Text(key = 'path')],
    [sg.Multiline(key = 'folder', size = (40,20)), sg.Listbox(filenames, key = 'folder', size = (40,20))],
    [sg.Button('Prev'), sg.Button('Play'), sg.Button('Next')],
    [sg.Submit(), sg.Button('Cancel')]
]

window = sg.Window('Python Music Player', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    elif event == 'Submit':
        foldername = values['FolderBrowse'] or '.'
        # window['path'].update('selected folder path: ',foldername)
        # filenames = os.listdir(foldername)
        filenames = os.walk(foldername)
        # window['folder'].update("\n".join(filenames))
        window['folder'].update(filenames)
        print(filenames)
        window['path'].update('selected folder path: ',foldername)

# https://github.com/PySimpleGUI/PySimpleGUI/issues/4393#issuecomment-859296723
# https://stackoverflow.com/questions/63725995/how-to-display-files-in-folder-when-using-pysimplegui-filebrowse-function
# To restrict a file type
# layout =  [[sg.In() ,sg.FileBrowse(file_types=(("Text Files", "*.txt"),))]]
window.close()
