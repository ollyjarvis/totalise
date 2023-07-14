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
        while finish == False:
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
                        
                case default:
                    quit()
                
    
def auth():
    if os.path.exists('oauth.json'):
        print('Using OAuth')
        try:
            ytmusic = YTMusic("oauth.json")
            return ytmusic
        except:
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
        
    option = input('Choose a function\n'+
                   '1 Fetch playlist from YouTube Music\n'+
                   '2 Export to CSV\n'+
                   '3 Quit\n'+
                   '\n')
    
    return option

def get_playlist(ytmusic):
    try:
        playlists = list(ytmusic.get_library_playlists())
    except:
        return 0
    count = 0
    
    out = 'Choose a playlist\n'
    for playlist in playlists:
        out = out + str(playlists.index(playlist)) + ' ' + playlist['title'] + '\n'
        count += 1
        
    option = input(out)
    try:
        option = int(option)
        if option <= count:
            playlist = playlists[option]
            return playlist
            
    except:
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
            line = unidecode(x[0].replace(',', '')) + ', ' + unidecode(x[1].replace(',', '')) + '\n'
            f.write(line)
        f.close()
        
    except:
        return 0

def make_safe_filename(s):
    def safe_char(c):
        if c.isalnum():
            return c
        else:
            return "_"
    return "".join(safe_char(c) for c in s).rstrip("_")
    
main()