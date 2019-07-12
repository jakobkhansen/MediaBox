# MediaBox
A project that strives to become a complete mediabox CLI, including movies, youtube, livestreams and whatever else I come up with. Specially designed to be used with a Raspberry Pi. Written entirely in Python 3

### Usage
Install VLC on raspberry pi or switch to omxplayer in settings.json (less features and worse stability)
```bash
$ pip3 -r requirements.txt
$ python3 main.py
```  

### SSH
This program connects to a raspberry pi using ssh and will automatically search for an ssh private key in ~/.ssh. If you want to specify a key or use a cleartext password instead (not recommended), set Search-SSH to false in settings.json and specify either a directory to a private-key or a password to connect with.  
Due to the way Paramiko (ssh client) validates RSA keys, a working ssh key may not be valid, try converting your private-key using:
```bash
$ ssh-keygen -p -m PEM -f ~/.ssh/id_rsa
```  
  
### Streaming to other devices
This tool could in theory (untested) be used to stream to any linux device as long as the device has omxplayer or VLC installed and ssh is enabled. Specify the ip and username in settings. I recommend setting up a static ip-address if your device does not have something similar to the pi's "raspberrypi.local" to find the ip.
