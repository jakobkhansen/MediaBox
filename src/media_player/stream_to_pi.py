from utils import utils
from paramiko import SSHClient, AutoAddPolicy, RSAKey
import threading, socketserver, socket, http.server
import json
import time
import os
import curses

import warnings
warnings.filterwarnings(action='ignore',module='.*paramiko.*')

def play_pi(video_path):

    settings = utils.load_settings()
    rasppi_settings = settings["raspberrypi"]
    port = rasppi_settings["media_serving_port"]
    host_ip = utils.get_ip()
    file_name = video_path.split("/")[-1]
    media_link = "http://{}:{}/{}".format(host_ip, port, file_name)
    flags = ["--timeout 30 "]

    http_thread = threading.Thread(target=http_server, args=(video_path, port))
    http_thread.daemon = True
    http_thread.start()
    ssh_client = connect_ssh(rasppi_settings)

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
    controller_loop(stdin)

def vlc_launch(ssh_client, media_link):
    flags = []
    launch = "vlc" + " ".join(flags) + media_link
    stdin, stdout, stderr = ssh_client.exec_command(launch)

    time.sleep(5)
    utils.clear_screen()
    controller_loop(stdin)



def controller_loop(stdin):
    while True:
        char = utils.getch()
        stdin.write(char)

        if (char == "q"):
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
    print(directory)
    os.chdir(directory)
    http_handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", port), http_handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()
