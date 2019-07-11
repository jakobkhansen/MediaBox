import vlc
import time
import keyboard
import os
from media_player.stream_to_pi import play_pi
from utils.utils import *

class MediaPlayer:
    def __init__(self):
        self._instance = vlc.Instance(["--video-on-top"])
        self._player = self._instance.media_player_new()
        self._player.set_fullscreen(True)
        self._enable_hotkeys()

    def start_playback(self, media_link):
        media = self._instance.media_new(media_link)
        self._player.set_media(media)
        self._player.play()

    def toggle_pause(self):
        self._player.pause()

    # def quit(self):
        # self._player.stop()

    def seek_forward(self):
        current_time = self._player.get_time()
        self._player.set_time(current_time + 10000)

    def seek_backward(self):
        current_time = self._player.get_time()
        self._player.set_time(current_time - 10000)

    def _enable_hotkeys(self):
        hotkeys = {
            "space":self.toggle_pause,
            "right":self.seek_forward,
            "left":self.seek_backward,
        }

        for hotkey in hotkeys.keys():
            keyboard.add_hotkey(hotkey, hotkeys[hotkey])

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











