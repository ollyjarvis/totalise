import os
from mutagen.flac import FLAC

def list_files(dir):
    r = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            r.append(os.path.join(root, name))
    return r

source_dir = input("Enter Directory to fix FROM: ")

count = 0

file_list = list_files(source_dir)

for f in file_list:
    if os.path.isfile(f) and f.endswith('.flac'):
        audio = FLAC(f)
        genres = []

        genres = audio["GENRE"]
        new_genre_list = []
        
        for i in genres: # type: ignore
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
            audio["GENRE"] = new_genre_list
            audio.save()
        
print("Finished, changed ", count, " files")
