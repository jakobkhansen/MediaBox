from utils import utils
from paramiko import SSHClient, AutoAddPolicy, RSAKey
import threading, socketserver, socket, http.server
import json
import time
import os, io, sys
import curses
import urllib

import warnings
warnings.filterwarnings(action='ignore',module='.*paramiko.*')

def play_pi(video_path):

    # Loading settings and information
    settings = utils.load_settings()
    rasppi_settings = settings["raspberrypi"]
    port = rasppi_settings["media_serving_port"]
    host_ip = utils.get_ip()
    file_name = video_path.split("/")[-1]

    # Encoding url
    media_link_unencoded = "http://{}:{}/{}".format(host_ip, port, file_name)
    media_link = urllib.parse.quote(media_link_unencoded, safe="/:")

    # Starting http server
    http_thread = threading.Thread(target=http_server, args=(video_path, port))
    http_thread.daemon = True
    http_thread.start()
    ssh_client = connect_ssh(rasppi_settings)

    # Launching on preferred_player
    players = {
        "vlc":vlc_launch,
        "omxplayer":omx_launch
    }

    pref_player = settings["streaming"]["preferred_player"]
    players[pref_player](ssh_client, media_link)

def omx_launch(ssh_client, media_link):

    flags = [" --timeout 30"]
    launch = "omxplayer" + " ".join(flags) + media_link
    stdin, stdout, stderr = ssh_client.exec_command(launch)

    time.sleep(5)
    utils.clear_screen()
    controller_loop_omx(stdin)

def vlc_launch(ssh_client, media_link):
    flags = ["-f", "-I rc"]
    launch = "DISPLAY=:0 vlc " + " ".join(flags) + " " + media_link
    print(launch)
    stdin, stdout, stderr = ssh_client.exec_command(launch)

    time.sleep(5)
    utils.clear_screen()
    controller_loop_vlc(stdin)



def controller_loop_omx(stdin):
    while True:
        char = utils.getch()
        stdin.write(char)

        if (char == "q"):
            break

def controller_loop_vlc(stdin):
    cases = {
        "p":["pause\n", "p"],
        " ":["pause\n", "space"],
        "q":["quit\n", "q"]
    }
    print("Controls:")
    for key in cases.keys():
        print("{} - {}".format(cases[key][1], cases[key][0]), end="")

    while True:
        try:
            char = utils.getch()
        except KeyboardInterrupt:
            break

        stdin.write(cases.get(char, "")[0])

        if char == "q":
            break

def connect_ssh(settings):

    ipaddr = settings["ip"]
    user = settings["username"]
    key = settings["SSH-key"]
    passw = settings["password"]
    look_keys = settings["Search-SSH"]

    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(AutoAddPolicy())

    ssh.connect(ipaddr, username=user, password=passw, key_filename=key, look_for_keys = look_keys)
    return ssh

def http_server(video_path, port):
    directory = "/".join(video_path.split("/")[:-1])
    os.chdir(directory)
    http_handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", port), http_handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()
