import PySimpleGUI as sg
import pygame as pg
from pygame import mixer
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
    [sg.Multiline(key = 'folder', size = (40,20)), \
     sg.Listbox(listvalues, key = 'files', size = (40,20))],
    [sg.Button('Play', key='pbutton'), sg.Button('Pause'), sg.Button('Stop'), \
     sg.Slider(range=(0,100), size=(50,20),  orientation='horizontal', resolution=1, enable_events=True, key = 'vslider', default_value=100)],
    [sg.Submit(), sg.Cancel()]
]

window = sg.Window('Python Music Player', layout, resizable=True, use_custom_titlebar=True, \
                   titlebar_icon='music_16px.png', \
                    titlebar_background_color='Black', titlebar_text_color='White', \
                        titlebar_font='Consolas', text_justification='center')

ispaused = ''

mixer.init()

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    elif event == 'Submit':
        foldername = values['FolderBrowse'] or '.'
        path = 'selected folder path: '+foldername
        window['path'].update(value = path)
        f = []
        paths = []
        songpaths = {}
        for (dirpath, dirnames, filenames) in os.walk(foldername):
            f.extend(filenames)
            paths.extend(dirnames)
            songpaths[dirpath] = filenames
        songkey = list(songpaths.keys())
        songvalue = list(songpaths.values())
        songvalue = songvalue[0]
        f = [file for file in f if file.endswith('.mp3'or'.wav'or'.aac')]
        listvalues = f
        window['folder'].update(paths)
        listvalues.append(values)
        window['files'].update(listvalues)
    elif event == 'pbutton':
        songfile = window['files'].get()[0]
        for i in songpaths.keys():
            for j in songpaths[i]:
                if j == songfile:
                    fpath = i+"/"+j
                    print("song path: ",fpath)
        mixer.music.load(fpath)
        mixer.music.set_volume(0.7)
        mixer.music.play()
        ispaused = False
    elif event == 'Pause':
        if mixer.music.get_busy() == True:
            ispaused = True
            mixer.music.pause()
        elif mixer.music.get_busy() != True:
            ispaused = False
            mixer.music.unpause()
    elif event == 'Stop':
        mixer.music.stop()
    elif event == 'vslider':
        volume = values['vslider']
        mixer.music.set_volume(volume/100)

window.close()
