import PySimpleGUI as sg
import pygame as pg
import glob
import os
import pathlib

sg.theme('DarkAmber')
sg.set_options(text_color=("Black"),\
               font=("Consolas", 10),\
                text_element_background_color=("Grey"))

listvalues = []

layout = [
    [sg.Text('Python Music Player!!', justification='center', size=(100,1))],
    [sg.FolderBrowse(key = 'FolderBrowse'), sg.Text(key = 'path')],
    [sg.Multiline(key = 'folder', size = (40,20)), sg.Listbox(listvalues, key = 'files', size = (40,20))],
    [sg.Button('Prev'), sg.Button('Play'), sg.Button('Next')],
    [sg.Submit(), sg.Button('Cancel')]
]

window = sg.Window('Python Music Player', layout, resizable=True)

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
        songvalue = songvalue[0]
        # print(glob.glob(foldername+'/*.*', recursive = True))
        listvalues = f
        window['folder'].update(paths)
        # listvalues.append(f)
        listvalues.append(values)
        window['files'].update(listvalues)
    elif event == 'Play':
        print("selected song: ",window['files'].get())
        songfile = window['files'].get()[0]
        for i in songpaths.keys():#songkey:
            for j in songpaths[i]:
                if j == songfile:
                    fpath = i+"/"+j
                    print("song path: ",fpath)
# import pprint
# pp = pprint.PrettyPrinter(indent = 0)
# pp.pprint(songkey)
# pp.pprint(songvalue)
# pp.pprint(songpaths)

window.close()
