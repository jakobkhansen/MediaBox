import libtorrent
import time

def download_torrent(torrent, directory):
    session = libtorrent.session()
    session.listen_on(6881, 6891)

    params = {
        "save_path": directory,
        "storage_mode": libtorrent.storage_mode_t(2),
        "paused": False,
        "auto_managed": True,
        "duplicate_is_error": True
    }
    magnet = torrent.magnet
    handle = libtorrent.add_magnet_uri(session, magnet, params)
    session.start_dht()

    print("Downloading metadata...")
    while (not handle.has_metadata()):
        time.sleep(1)

    print("Starting torrent download...")

    while (handle.status().state != libtorrent.torrent_status.seeding):
        s = handle.status()
        state_str = ['queued', 'checking', 'downloading metadata', \
            'downloading', 'finished', 'seeding', 'allocating']
        print("%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s" % \
            (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
            s.num_peers, state_str[s.state]))
        time.sleep(5)
    
    print("Torrent downloaded")


