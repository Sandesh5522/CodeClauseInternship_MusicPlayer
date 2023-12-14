import PySimpleGUI as sg
import pygame as pg
import glob
import os
import pathlib

sg.theme('DarkAmber')

listvalues = []

layout = [
    [sg.Text('Python Music Player!!', justification='center', size=(100,1))],
    [sg.FolderBrowse(key = 'FolderBrowse'), sg.Text(key = 'path')],
    [sg.Multiline(key = 'folder', size = (40,20)), sg.Listbox(listvalues, key = 'files', size = (40,20))],
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
        # files = os.walk(foldername)
        f = []
        paths = []
        songpaths = {}
        for (dirpath, dirnames, filenames) in os.walk(foldername):
            f.extend(filenames)
            paths.extend(dirnames)
            songpaths[dirpath] = filenames
            # print("D:/SONGS/HINDI SONGS/",dirpath,"/",dirnames,"/",filenames)
            # print(os.path.abspath(filenames[0]))
            # print(os.path.join(dirpath[0], filenames[0]))
        # print(glob.glob('D:/SONGS/HINDI SONGS/*.*'))
        songkey = list(songpaths.keys())
        songvalue = list(songpaths.values())
        print(songpaths)
        print(songkey)
        print(songvalue)
        # print(glob.glob(foldername+'/*.*', recursive = True))
        # print(paths)
        listvalues = f
        window['folder'].update(paths)
        # listvalues.append(f)
        listvalues.append(values)
        window['files'].update(listvalues)
    elif event == 'Play':
        print("selected song: ",window['files'].get())
        songfile = window['files'].get()[0]
        spath = 'D:/SONGS/HINDI SONGS/*.'+songfile
        # print(glob.glob(spath))
        spath = pathlib.Path('.').glob('**/'+songfile+'.mp3')
        for k,v in songpaths.items():
            if songfile == v:
                print(k)
        print(songkey[songvalue.index(songfile)])
        # print(spath)


# https://github.com/PySimpleGUI/PySimpleGUI/issues/4393#issuecomment-859296723
# https://stackoverflow.com/questions/63725995/how-to-display-files-in-folder-when-using-pysimplegui-filebrowse-function
# To restrict a file type
# layout =  [[sg.In() ,sg.FileBrowse(file_types=(("Text Files", "*.txt"),))]]
window.close()
