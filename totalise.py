import os
from mutagen.flac import FLAC

def list_files(dir):
    r = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            r.append(os.path.join(root, name))
    return r

source_dir = input("Enter Directory to move FROM: ")
music_dir = input("Enter Directory to move TO: ")

count = 0

file_list = list_files(source_dir)

for f in file_list:
    parsed_f = os.path.split(f)[1]
    if os.path.isfile(f) and os.path.splitext(f)[1] == '.flac':
        audio = FLAC(f)
        artist = audio.tags['artist'][0].replace('/', '_').replace('\\' , '_').strip() # type: ignore
        new_dir = os.path.join(music_dir, artist)
        genres = audio.tags['genre'] # type: ignore
        new_genre_list = []

        for i in genres:
            new_genre_list.append(i)
            split_genres = []
            
            if '&' in i and "R&B" not in i:
                split_genres = i.split('&')
                new_genre_list.remove(i)
                
                for x in split_genres:
                    new_genre_list.append(x.strip())
                count += 1
                
            if '/' in i:
                split_genres = i.split('/')
                new_genre_list.remove(i)

                for x in split_genres:
                    new_genre_list.append(x.strip())
                count += 1
                
            if i == 'Progressive Rock':
                new_genre_list.remove(i)
                new_genre_list.append('Rock')
                
            if i == 'Hard Rock':
                new_genre_list.remove(i)
                new_genre_list.append('Rock')

            if i == 'Contemporary Jazz':
                new_genre_list.remove(i)
                new_genre_list.append('Jazz')

            if i == 'New Wave':
                new_genre_list.remove(i)
                new_genre_list.append('Rock')
                new_genre_list.append('Punk')
                
                for x in split_genres:
                    new_genre_list.append(x.strip())
                count += 1

        if new_genre_list != genres:
            print("Changed ", f)
            audio.tags['genre'] = new_genre_list # type: ignore
            audio.save()
        
        if os.path.exists(new_dir) == False:
            os.mkdir(new_dir)
            print("Directory '% s' created" % new_dir)
            
        if os.path.isfile(os.path.join(new_dir, parsed_f)) == False:
            os.rename(f, os.path.join(new_dir, parsed_f))
            count += 1
        else:
            print("Skipped ", parsed_f, " \nFile of same name in output folder !")

print("Finished, moved ", count, " files")
