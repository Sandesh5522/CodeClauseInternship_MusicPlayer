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
                text_element_background_color=("Grey"), margins=(5,5,5,5), auto_size_buttons=True, auto_size_text=True)

foldernames = []
listvalues = []

layout = [
    [sg.Text('Python Music Player!!', justification='center', size=(100,1))],
    [sg.FolderBrowse(key = 'FolderBrowse'), sg.Text('Selected Folder path: ',key = 'path')],
    [sg.Text('Now playing: ',key='now_playing')],
    [sg.Listbox(foldernames, key = 'folder', size = (40,20)), \
     sg.Listbox(listvalues, key = 'files', size = (60,20))], #highlight_background_color='Grey', background_color='Black', text_color='Grey', highlight_text_color='Black'
    [sg.Button('Play'), sg.Button('Pause'), sg.Button('Stop'), \
     sg.Button('Prev'), sg.Button('Next'), sg.Button('Minimize')],
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

def songplay(f : list, songpaths : dict, songfile : str, o : int):
    for i in f:
        if i == songfile:
            current_index = f.index(i)
            if o == 1:
                current_index = current_index + 1
            elif o == -1:
                current_index = current_index - 1
    songname = f[current_index]
    for i in songpaths.keys():
            for j in songpaths[i]:
                if j == songname:
                    fpath = i+"/"+j
                    # print("song path: ",fpath)
    return [songname, current_index, fpath]

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
            window['Pause'].update('Resume')
            mixer.music.pause()
        elif mixer.music.get_busy() != True:
            window['Pause'].update('Pause')
            mixer.music.unpause()
    elif event == 'Stop':
        mixer.music.stop()
    elif event == 'Prev':
        details = songplay(f, songpaths, songfile, -1)
        songfile = details[0]
        window['now_playing'].update("Now playing: "+details[0])
        window['files'].update(set_to_index=details[1])
        mixer.music.load(details[2])
        mixer.music.play()
    elif event == 'Next':
        details = songplay(f, songpaths, songfile, 1)
        songfile = details[0]
        window['now_playing'].update("Now playing: "+details[0])
        window['files'].update(set_to_index=details[1])
        mixer.music.load(details[2])
        mixer.music.play()
    elif event == 'vslider':
        volume = values['vslider']
        mixer.music.set_volume(volume/100)
    elif event == 'Minimize':
        window['folder'].set_size(size=(40,4))
        window['files'].set_size(size=(40,4))

window.close()
