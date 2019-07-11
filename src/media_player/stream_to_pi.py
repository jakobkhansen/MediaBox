from utils.utils import *
from paramiko import SSHClient, AutoAddPolicy, RSAKey
import threading, socketserver, socket, http.server
import json
import time
import os
import curses

import warnings
warnings.filterwarnings(action='ignore',module='.*paramiko.*')

def play_pi(video_path):

    settings = load_settings()["raspberrypi"]
    port = settings["media_serving_port"]
    host_ip = get_ip()
    file_name = video_path.split("/")[-1]
    media_link = "http://{}:{}/{}".format(host_ip, port, file_name)
    flags = ["--timeout 30 "]

    http_thread = threading.Thread(target=http_server, args=(video_path, port))
    http_thread.daemon = True
    http_thread.start()
    ssh_client = connect_ssh(settings)

    vlc_launch = "omxplayer " + " ".join(flags) + media_link
    print(vlc_launch)

    stdin, stdout, stderr = ssh_client.exec_command(vlc_launch)

    time.sleep(5)
    # clear_screen()
    controller_loop(stdin)


def controller_loop(stdin):
    while True:
        char = getch()
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