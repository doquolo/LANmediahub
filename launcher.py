# TODO: write a GUI script which allow the server to run with windows and be able to change database location
import PySimpleGUI as sg
import os
import json
from main import app
import threading
import sys
from io import StringIO


def setup():
    # indexing all files in the folder
    # Specify the folder path
    folder_path = 'assets'

    # Walk through the folder and its subdirectories
    res = []
    for root, dirs, files in os.walk(folder_path):
        layout = [
            [sg.Text("Start indexing the media files!")],
            [sg.ProgressBar(len(files), key="-ProgressBar-")],
            [sg.Text("", key="-status-")]
        ]
        win = sg.Window("Indexing", layout, finalize=True)
        i, fileLen = 0, len(files)
        while True:
            e, v = win.read(timeout=10)

            if i < fileLen:
                file = files[i]
                file_path = os.path.join(root, file)
                path = os.path.dirname(file_path)
                win['-status-'].update(f"Indexing: {file_path}")

                video_extensions = ["mp4", "avi", "mkv", "mov", "wmv"]
                extension = file.split(".")[1]
                if extension != "json":
                    if extension in video_extensions:
                        res.append([file, path, "video"])
                    else:
                        res.append([file, path, "image"])
                i += 1
                win['-ProgressBar-'].update(i)
            else: 
                win.close()
                break
    
    with open("assets/index.json", "w") as file:
        file.write(json.dumps(res))

def startServer():
    server_up = False
    # Define the layout of your window
    layout = [
        [sg.Text("Path to database folder: assets/", enable_events=True, key="-folder-")],
        [sg.Button('Run', key="-run-"), sg.Button('Exit')],
        [sg.Text("Server Log:")],
        [sg.Multiline(size=(120, 20), key="-output-", background_color="#000", text_color="#ffb6c1", reroute_stdout=True, reroute_stderr=True, reroute_cprint=True, auto_size_text=True, autoscroll=True)],
    ]

    # Create the window
    window = sg.Window('Terminal Output', layout)

    # Event loop to process events and display output
    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, 'Exit'):
            window.close()
            os._exit(1)
        elif event == '-folder-':
            os.startfile("assets")
        elif event == '-run-':
            # start server
            def runApp():
                app.run(host="0.0.0.0", use_reloader=False)
            server = threading.Thread(target=runApp)
            server.start()  

            # gray out the run button
            window["-run-"].update(disabled=True)

    


def checkInit():
    if (not os.path.isdir("assets/")):
        content = "LANmediahub cannot find assets/\nCreate one?"
        choice = sg.popup_ok_cancel(content, title="Setup - Alert")
        if (choice == "OK"):
            os.mkdir("assets/")
        else:
            raise SystemExit(0)
    if (not os.path.isfile("assets/index.json")):
        content = "It seems that this is the first time you start up LANmediahub\nBegin setup process?"
        choice = sg.popup_ok_cancel(content, title="Setup - Alert")
        if (choice == "OK"):
            setup()
        else:
            raise SystemExit(0)
    
    # start server
    startServer()


if (__name__ == "__main__"):
    checkInit()