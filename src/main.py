from utils.utils import *
from media_player import player
import os, sys


def unimplemented():
    print("Unimplemented")

def main():
    clear_screen()
    print("Welcome to MediaBox, what do you want to do?\n")

    menu_items = {
        "Download movie":unimplemented,
        "Play local media":player.player_menu,
        "Settings":unimplemented,
        "Exit MediaBox":sys.exit,
    }
    function_to_exec = menu(menu_items)
    function_to_exec()


if __name__ == "__main__":
    main()
