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
flac_file_list = []

for file in file_list:
    if os.path.isfile(file) and os.path.splitext(file)[1] == '.flac':
        flac_file_list.append(file)

for f in flac_file_list:
    parsed_f = os.path.split(f)[1]
    audio = FLAC(f)
    artist = audio.tags['artist'][0]
    artist = artist.replace('/', '_').replace('\\', '_').strip()
    new_dir = os.path.join(music_dir, artist)
    try:
        genres = audio.tags['genre']
    except Exception:
        genres = []

    new_genre_list = []

    if genres == []:
        print(parsed_f)
        tags = input(print(
            "File has no genre tags, Enter genres separated by Comma: ")
                         ).split(',')
        for genre in tags:
            new_genre_list.append(genre.strip())

    for i in genres:
        new_genre_list.append(i)
        split_genres = []

        match i:
            case 'Miscellaneous':
                new_genre_list.remove(i)
            case 'New Wave':
                new_genre_list.remove(i)
                new_genre_list.append('Rock')
                new_genre_list.append('Punk')
            case 'Trip Hop':
                new_genre_list.remove(i)
                new_genre_list.append('Hip-Hop')
                new_genre_list.append('Dance')
            case 'Trip-Hop':
                new_genre_list.remove(i)
                new_genre_list.append('Hip-Hop')
                new_genre_list.append('Dance')
            case 'World':
                new_genre_list.remove(i)
            case 'Alternatif et Indé':
                new_genre_list.remove(i)
                new_genre_list.append('Alternative')
                new_genre_list.append('Indie')
            case'Avant-Garde':
                new_genre_list.remove(i)
            case 'French Music':
                new_genre_list.remove(i)
            case 'House':
                new_genre_list.remove(i)
                new_genre_list.append('Dance')

        if '&' in i and "R&B" not in i:
            split_genres = i.split('&')
            new_genre_list.remove(i)

            for x in split_genres:
                new_genre_list.append(x.strip())
            count += 1

        elif '/' in i:
            split_genres = i.split('/')
            new_genre_list.remove(i)

            for x in split_genres:
                new_genre_list.append(x.strip())
            count += 1

        elif ',' in i:
            split_genres = i.split(',')
            new_genre_list.remove(i)

            for x in split_genres:
                new_genre_list.append(x.strip())
            count += 1

        elif 'Rock' in i and 'Rock' != i:
            new_genre_list.remove(i)
            new_genre_list.append('Rock')

        elif 'Jazz' in i and 'Jazz' != i:
            new_genre_list.remove(i)
            new_genre_list.append('Jazz')

        elif 'Film' in i:
            new_genre_list.remove(i)

    if new_genre_list != genres:
        audio.save()
    if os.path.exists(new_dir) is False:
        os.mkdir(new_dir)
    if os.path.isfile(os.path.join(new_dir, parsed_f)) is False:
        os.rename(f, os.path.join(new_dir, parsed_f))
        count += 1

print("Finished, moved ", count, " files")

empty = []

empty = [root for root, dirs, files,
         in os.walk(music_dir)if not len(dirs) and not len(files)]

for folder in empty:
    os.rmdir(folder)
    print('Removed ', folder, 'as it is now empty')
