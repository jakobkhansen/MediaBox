from collections import OrderedDict
import json
import sys, os, termios, tty
import socket

def menu(menu_items):

    ordered = OrderedDict(menu_items)

    while True:
        for index, description in enumerate(ordered.keys()):
            print("{} - {}".format(index+1, description))
        
        selected = int(input("\nPick option: ")) - 1

        if selected >= 0 and selected < len(ordered):
            function = ordered[list(ordered.keys())[selected]]
            return function
        else:
            print("Invalid index")

def file_menu(files):
    file_names = [file[-1] for file in [file.split("/") for file in files]]

    for index, name in enumerate(file_names):
        print("{} - {}".format(index+1, name))

    selected = int(input("\nPick option: ")) - 1

    if selected >= 0 and selected < len(files):
        return files[selected]
    else:
        print("Invalid index")


def load_settings():
    json_string = open('settings.json').read()
    settings = json.loads(json_string)
    return settings

def clear_screen():
    os.system("clear")
    print("--- MEDIABOX ---")

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
