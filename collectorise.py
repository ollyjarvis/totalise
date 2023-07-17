from ytmusicapi import YTMusic
import os
from unidecode import unidecode


def main():
    ytmusic = auth()
    if ytmusic == 0:
        quit()
    playlist = {}
    finish = False
    if type(ytmusic) == YTMusic:
        print('Authorised')
        while finish is False:
            option = menu(playlist)
            match option:
                case '1':
                    done = get_playlist(ytmusic)
                    if done == 0:
                        print("Couldn't get playlist(s)")
                    else:
                        print('Completed task\n\n')
                        playlist = done
                case '2':
                    done = export_playlist(ytmusic, playlist)
                    if done == 0:
                        print("Couldn't export playlist")
                    else:
                        print('Completed task\n\n')
                case '3':
                    done = fix_playlist(ytmusic, playlist)
                    if done == 0:
                        print("Couldn't export playlist")
                    else:
                        print('Completed task\n\n')
                case _:
                    quit()


def auth():
    if os.path.exists('oauth.json'):
        print('Using OAuth')
        try:
            ytmusic = YTMusic("oauth.json")
            return ytmusic
        except Exception:
            pass

    else:
        print('Generating OAuth token')
        os.system('ytmusicapi oauth')
        if os.path.exists('oauth.json'):
            main()
    return 0


def menu(playlist):
    if playlist != {}:
        print('Current playlist is: ' + playlist['title'] + '\n')
    option = input('Choose a function\n' +
                   '1 Fetch playlist from YouTube Music\n' +
                   '2 Export to CSV\n' +
                   '3 Fix Playlist\n' +
                   '4 Quit\n' +
                   '\n')
    return option


def get_playlist(ytmusic):
    try:
        playlists = list(ytmusic.get_library_playlists())
    except Exception:
        return 0
    count = 0
    out = 'Choose a playlist\n'
    for playlist in playlists:
        out = out + str(playlists.index(playlist))
        out = out + ' ' + playlist['title'] + '\n'
        count += 1
    option = input(out)
    try:
        option = int(option)
        if option <= count:
            playlist = playlists[option]
            return playlist
    except Exception:
        return 0


def export_playlist(ytmusic, playlist):
    if playlist == {}:
        print('No current playlist. Get playlist first')
        return 0
    songs = []
    try:
        playlist_info = dict(ytmusic.get_playlist(playlist['playlistId']))
        songs = playlist_info['tracks']
        songs_list = []
        title_artist = ['Title', 'Artist']

        songs_list.append(title_artist)

        for song in songs:
            entry = []
            artists = {}
            artists = song['artists']
            entry.append(song['title'])
            entry.append(artists[0]['name'])
            songs_list.append(entry)

        filename_noext = playlist_info['title']
        filename = make_safe_filename(filename_noext) + '.csv'

        count = 0

        while os.path.exists(filename):
            print('File exists')
            filename = make_safe_filename(filename_noext + str(count)) + '.csv'
            count += 1

        f = open(filename, "w")

        for x in songs_list:
            line = unidecode(x[0].replace(',', '')) + ', '
            line = line + unidecode(x[1].replace(',', '')) + '\n'
            f.write(line)

        f.close()

    except Exception:
        return 0


def fix_playlist(ytmusic, playlist):
    if playlist == {}:
        print('No current playlist. Get playlist first')
        return 0

    songs = []
    switch = []

    playlist_info = dict(ytmusic.get_playlist(playlist['playlistId']))
    songs = playlist_info['tracks']
    songs_list = []
    title_artist = ['Title', 'Artist', 'Album']

    songs_list.append(title_artist)

    for song in songs:
        entry = []
        artists = {}

        artists = song['artists']

        entry.append(song['title'])
        entry.append(artists[0]['name'])
        entry.append(song['album'])

        songs_list.append(entry)

    for entry in songs_list:
        if entry[2] is None:
            print('Music Video to replace', entry[0], entry[1])

            query = entry[0] + ' ' + entry[1]
            results = ytmusic.search(query=query, filter='songs')
            out = ('1 ' + results[0]['title'] +
                   results[0]['artists'][0]['name'] + '\n' +
                   '2 ' + results[1]['title'] +
                   results[1]['artists'][0]['name'] + '\n' +
                   '3 ' + results[2]['title'] +
                   results[2]['artists'][0]['name'] + '\n')
            print(out)
            choice = input('4 Skip')
            change = True

            match choice:
                case '1':
                    new_id = results[0]['videoId']
                case '2':
                    new_id = results[1]['videoId']
                case '3':
                    new_id = results[2]['videoId']
                case _:
                    change = False

            if change is True:
                old_new = [songs_list.index(entry - 1), new_id]
                switch.append(old_new)

        for song in switch:
            old_song = []
            old_song.append(songs[song[0]])
            print('Removing ' + str(old_song))
            # ytmusic.remove_playlist_items(playlist['playlistId'], old_song)
            
            new_song = []
            new_song.append(song[1])
            print('Adding ' + str(new_song))
            ytmusic.add_playlist_items(playlist['playlistId'], new_song)
    try:
        return 0
    except Exception:
        return 0


def make_safe_filename(s):
    def safe_char(c):
        if c.isalnum():
            return c
        else:
            return "_"
    return "".join(safe_char(c) for c in s).rstrip("_")


main()
