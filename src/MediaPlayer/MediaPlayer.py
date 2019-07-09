import vlc
import time
import keyboard

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


def main():
    player = MediaPlayer()
    player.start_playback("/home/jakob/Downloads/TheOfficeSeason2/episode1.avi")



    keyboard.wait("q")

main()


