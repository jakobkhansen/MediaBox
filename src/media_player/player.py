import time
import os
from media_player.stream_to_pi import play_pi
from utils.utils import *

def play_locally(video_path):
    print("play locally")

def select_videofile(directory):
    videos = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Better way to find videofiles would be good
            if file.endswith((".mp4", ".mkv", "avi")):
                videos.append(os.path.join(root, file))

    clear_screen()
    return file_menu(videos)


def player_menu():

    video_dir = os.path.expanduser(load_settings()["files"]["video_directory"])
    video_path = select_videofile(video_dir)
    print(video_path)

    menu_items = {
        "Play media locally":play_locally,
        "Send media to Raspberry pi":play_pi,
    }
    clear_screen()
    function_to_exec = menu(menu_items)
    function_to_exec(video_path)











