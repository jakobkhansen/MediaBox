from collections import OrderedDict
import sys

def menu():
    menu_items = {
        "Download movie":unimplemented,
        "Play local media":unimplemented,
        "Settings":unimplemented,
        "Exit MediaBox":sys.exit,
    }

    ordered = OrderedDict(menu_items)

    while True:
        for index, description in enumerate(ordered.keys()):
            print("{} - {}".format(index+1, description))
        
        selected = int(input("\nPick option: ")) - 1

        if selected >= 0 and selected < len(ordered):
            function = ordered[list(ordered.keys())[selected]]
            function()
        else:
            print("Invalid index")


def unimplemented():
    print("Unimplemented")


def main():
    print("Welcome to MediaBox, what do you want to do?\n")
    menu()


if __name__ == "__main__":
    main()
