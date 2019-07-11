import yify

def search_movie(movie_title):
    movie_list = yify.search_movies(movie_title)

    print("Movies:")
    counter = 1
    for movie in movie_list:
        print(str(counter) + ": " + str(movie))
        counter += 1
    print()

    movie_index = int(input("Select movie by number: ")) - 1
    if movie_index >= 0 and movie_index < len(movie_list):
        movie = movie_list[movie_index]
        print("Movie selected: " + str(movie))
    else:
        print("Invalid index, aborting...")
        return

    torrents = movie.torrents
    
    print("\nTorrents")
    counter = 1
    for torrent in torrents:
        print(str(counter) + ": " + str(torrent))
        counter += 1
    print()

    torrent_index = int(input("Select torrent by number: ")) - 1
    if torrent_index >= 0 and torrent_index < len(torrents):
        return torrents[torrent_index]
    else:
        print("Invalid index, aborting")


