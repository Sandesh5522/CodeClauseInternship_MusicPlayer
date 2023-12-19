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
            #    Some good fonts.
            #    font=("Consolas", 10),\
            #    font=("Constantia", 10), \
                font=("Bahnschrift", 10), \
                text_element_background_color=("Grey"), margins=(5,5,5,5))

foldernames = []
listvalues = []

layout = [
    [sg.Text('Python Music Player!!', justification='center', size=(100,1))],
    [sg.FolderBrowse(key = 'FolderBrowse'), sg.Text(key = 'path')],
    [sg.Listbox(foldernames, key = 'folder', size = (40,20)), \
     sg.Listbox(listvalues, key = 'files', size = (60,20))],
    [sg.Button('Play'), sg.Button('Pause'), sg.Button('Stop'),
     sg.Slider(range=(0,100), size=(50,20),  orientation='horizontal', resolution=1, \
        enable_events=True, key = 'vslider', default_value=100)],
    [sg.Submit(), sg.Cancel()]
]

window = sg.Window('Python Music Player', layout, resizable=True, \
                #   Turn custom titlebar on to see the custom titlebar
                #   but the custom titlebar dosent show the logo on taskbar.
                    # use_custom_titlebar=True, \
                    titlebar_icon='music_16px.png', \
                    # icon file names icons8_music.ico music_16px.png
                    icon='icons8_music.ico', \
                    # titlebar_background_color='Black', titlebar_text_color='White', \
                    # titlebar_font='Consolas', 
                    # titlebar_font="Constantia", text_justification='center'
                    )

mixer.init()

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    elif event == 'Submit':
        foldername = values['FolderBrowse'] or '.'
        path = 'Selected folder path: '+foldername
        window['path'].update(value = path)
        f = []
        paths = []
        songpaths = {}
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
    elif event == 'vslider':
        volume = values['vslider']
        mixer.music.set_volume(volume/100)

window.close()
