from subliminal import Video, download_best_subtitles, save_subtitles
from babelfish import Language
import os


def find_subs(filename, movie_dir):
    video = Video.fromname(filename)
    subtitles = download_best_subtitles([video], {Language("eng")})

    if len(subtitles[video]) == 0:
        print("No subs found")
        return

    best_sub = subtitles[video][0]
    save_subtitles(video, [best_sub], directory=movie_dir)
    return get_sub_path(movie_dir)


# TODO: Give option to select subfiles?
def get_sub_path(movie_dir):

    # Find first subtitle file and break

    subpath = None
    for root, dirs, files in os.walk(movie_dir):
        for file in files:
            if file.endswith(".srt"):
                subpath = os.path.join(root, file)
                break
    return subpath.replace(os.getcwd(), "")
