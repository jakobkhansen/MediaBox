import sys, os
from search import search_movie
from download import download_torrent
from subliminal import download_best_subtitles, Video
from babelfish import Language
from subs import find_subs

def main():
    if len(sys.argv) > 1:
        torrent = search_movie(sys.argv[1])
    else:
        print("No argument found, using manual search term")
        search_term = input("Movie search term: ")
        torrent = search_movie(search_term)

    # The directory command was run from
    current_dir = os.getcwd()

    # We create a directory to download the torrent in
    movie_dir = current_dir + "/" + torrent.name

    download_torrent(torrent, movie_dir)

    videofile = find_videofile(movie_dir).replace(current_dir, "")
    filename = videofile.split("/")[-1]

    print("Downloading subs...")
    subs = find_subs(filename, movie_dir)




def find_videofile(movie_dir):

    videos = []
    for root, dirs, files in os.walk(movie_dir):
        for file in files:
           # Better way to find videofiles would be good
           if file.endswith((".mp4", ".mkv", "avi")):
               videos.append(os.path.join(root, file))

    if len(videos) == 1:
        videofile = videos[0]

    elif len(videos) == 0:
        print("No videofile found, aborting...")
        return
    else:
        counter = 1
        for video in videos:
            print(str(counter) + ": " + video)
        videofile_index = int(input("\nSelect videofile by number: ")) - 1
        if videofile_index >= 0 and videofile_index < len(videos):
            videofile = videos[videofile_index]
        else:
            print("Invalid index, aborting...")
            return
    return videofile


if __name__ == "__main__":
    main()
