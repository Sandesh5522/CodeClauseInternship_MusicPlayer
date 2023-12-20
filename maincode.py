import PySimpleGUI as sg
from pygame import mixer
import os

import sys

# This bit gets the taskbar icon working properly in Windows.
if sys.platform.startswith('win'):
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(u'CompanyName.ProductName.SubProduct.VersionInformation') # Arbitrary string

sg.theme('DarkAmber')
sg.set_options(text_color=("Black"),\
            #   Some good fonts.
                # font=("Consolas", 10), \
                # font=("Constantia", 10), \
                font=("Bahnschrift", 10), \
                text_element_background_color=("Grey"), margins=(5,5,5,5))

foldernames = []
listvalues = []

layout = [
    [sg.Text('Python Music Player!!', justification='center', size=(100,1))],
    [sg.FolderBrowse(key = 'FolderBrowse'), sg.Text('Selected Folder path: ',key = 'path')],
    [sg.Text('Now playing: ',key='now_playing')],
    [sg.Listbox(foldernames, key = 'folder', size = (40,20)), \
     sg.Listbox(listvalues, key = 'files', size = (60,20))],
    [sg.Button('Play'), sg.Button('Pause'), sg.Button('Stop'), sg.Button('Prev'), sg.Button('Next')],
    [sg.Slider(range=(0,100), size=(50,20),  orientation='horizontal', resolution=1, \
        enable_events=True, key = 'vslider', default_value=100)],
    [sg.Submit(), sg.Cancel()]
]

window = sg.Window('Python Music Player', layout, resizable=True, \
                #   Turn custom titlebar on to see the custom titlebar
                #   but the custom titlebar dosent show the logo on taskbar.
                    # use_custom_titlebar=True, \
                    titlebar_icon='music_16px.png', \
                #   icon file names music_16px.png icons8_music_64px.ico
                    icon='icons8_music_64px.ico', \
                    titlebar_background_color='Black', titlebar_text_color='White', \
                    # titlebar_font='Consolas', 
                    titlebar_font="Constantia", text_justification='center'
                    )

mixer.init()

f = []
paths = []
songpaths = {}

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    elif event == 'Submit':
        foldername = values['FolderBrowse'] or '.'
        window['path'].update('Selected folder path: '+foldername)
        for (dirpath, dirnames, filenames) in os.walk(foldername):
            f.extend(filenames)
            paths.extend(dirnames)
            songpaths[dirpath] = filenames
        f = [file for file in f if file.endswith('.mp3'or'.wav'or'.aac')]
        listvalues = f
        foldernames = paths
        window['folder'].update(foldernames)
        listvalues.append(values)
        window['files'].update(listvalues)
    elif event == 'Play':
        songfile = window['files'].get()[0]
        window['now_playing'].update("Now playing: "+songfile)
        for i in songpaths.keys():
            for j in songpaths[i]:
                if j == songfile:
                    fpath = i+"/"+j
                    print("song path: ",fpath)
        mixer.music.load(fpath)
        mixer.music.play()
    elif event == 'Pause':
        if mixer.music.get_busy() == True:
            mixer.music.pause()
        elif mixer.music.get_busy() != True:
            mixer.music.unpause()
    elif event == 'Stop':
        mixer.music.stop()
    elif event == 'Prev':
        for i in f:
            if i == songfile:
                current_index = f.index(i)
                current_index = current_index-1
        prev_song = f[current_index]
        window['now_playing'].update("Now playing: "+prev_song)
        for i in songpaths.keys():
            for j in songpaths[i]:
                if j == prev_song:
                    fpath = i+"/"+j
                    print("song path: ",fpath)
        window['files'].update(set_to_index=current_index)
        mixer.music.load(fpath)
        mixer.music.play()
    elif event == 'Next':
        for i in f:
            if i == songfile:
                current_index = f.index(i)
                current_index = current_index+1
        next_song = f[current_index]
        window['now_playing'].update("Now playing: "+next_song)
        for i in songpaths.keys():
            for j in songpaths[i]:
                if j == next_song:
                    fpath = i+"/"+j
                    print("song path: ",fpath)
        window['files'].update(set_to_index=current_index)
        mixer.music.load(fpath)
        mixer.music.play()
    elif event == 'vslider':
        volume = values['vslider']
        mixer.music.set_volume(volume/100)

window.close()
