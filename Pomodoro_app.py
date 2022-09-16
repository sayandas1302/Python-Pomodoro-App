from asyncio.windows_events import NULL
import PySimpleGUI as sg
from time import time

# function to convert the seconds into %2d:%2d format for timer display
def transform_into_elasped(seconds):
    min = '0' + str(seconds//60) if len(str(seconds//60)) != 2 else str(seconds//60)
    sec = '0' + str(seconds%60) if len(str(seconds%60)) != 2 else str(seconds%60)
    return f'{min}:{sec}'

# fuction to create a window with specified layout
def create_window():
    # layout
    layout = [
        [sg.VPush(background_color = '#FFE9A0')],
        [sg.Text('00:00', 
                  key='-TIMER-', 
                  font='Helvetica 35 bold', 
                  background_color = '#FFE9A0', 
                  text_color='#874C62')],
        [sg.Image('bckgrnd1.png', background_color='#FFE9A0')],
        [sg.Text('Start me!', 
                 key='-STATUS-', 
                 font='Helvetica 12 bold', 
                 background_color = '#FFE9A0',
                 text_color = '#874C62')],
        [sg.Button('Start', 
                    key='-START-', 
                    font = 'Helvetica 12 bold',
                    button_color=['#FFFFFF', '#3D8361'], 
                    border_width=0), 
         sg.Button('Reset', 
                    key='-RESET-', 
                    font = 'Helvetica 12 bold',
                    button_color=['#FFFFFF', '#3D8361'], 
                    border_width=0)],
        [sg.VPush(background_color = '#FFE9A0')],
    ]

    # the window
    return sg.Window('Pomodoro App', 
                    layout,
                    size=(300, 300),
                    element_justification='center',
                    background_color = '#FFE9A0')

# app variables
window = create_window()
work_active = False
rest_active = False
rest_count = 0
start = NULL
future = NULL
status = NULL
textcolor = NULL

# app constants
WORK = 25*60
SMALL_REST = 5*60
BIG_REST = 20*60

# main loop
while True:
    event, values = window.read(timeout=10)

    if event == sg.WIN_CLOSED:
        break

    if event == '-START-':
        start = time()
        future = start + WORK
        work_active = True
        status = 'WORK'
        textcolor = '#CC3636'

    if event == '-RESET-':
        window.close()
        window = create_window()
        work_active = False
        rest_active = False
        rest_count = 0
        start = NULL
        future = NULL
        status = NULL
        textcolor = NULL

    if work_active:
        window['-STATUS-'].update(status, text_color=textcolor)
        now = time()
        elasped = transform_into_elasped(round(now - start))
        if now <= future:
            window['-TIMER-'].update(elasped)
        else:
            work_active = False
            rest_active = True
            rest_count += 1
            start = time()
            future = start + SMALL_REST if rest_count%4 != 0 else start + BIG_REST
            status = 'SMALL REST' if rest_count%4 != 0 else 'BIG REST'
            textcolor = '#F57328' if rest_count%4 != 0 else '#1C6758'

    if rest_active:
        window['-STATUS-'].update(status, text_color=textcolor)
        now = time()
        elasped = transform_into_elasped(round(now - start))
        if now <= future:
            window['-TIMER-'].update(elasped)
        else:
            work_active = True
            rest_active = False
            start = time()
            future = start + WORK
            status = 'WORK'
            textcolor = '#CC3636'

# closing the window
window.close()