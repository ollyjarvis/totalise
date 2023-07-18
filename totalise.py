import os
from mutagen.flac import FLAC


def main():
    source_dir = input("Enter Directory to move FROM: ")
    music_dir = input("Enter Directory to move TO: ")

    file_list = list_files(source_dir)

    file_info = get_metadata(file_list, music_dir)

    make_dirs(file_info)

    edit_genres(file_info)

    move_files(file_info)

    remove_empty_dir(source_dir)
    remove_empty_dir(music_dir)


def list_files(dir):
    r = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            if os.path.splitext(name)[1] == '.flac':
                r.append(os.path.join(root, name))
    return r


def get_metadata(files, music_dir):
    file_info = []
    for f in files:
        file = []
        audio = FLAC(f)

        artist = audio.tags['artist'][0]
        artist = artist.replace('/', '_').replace('\\', '_').strip()
        new_dir = os.path.join(music_dir, artist)

        file.append(f)
        file.append(new_dir)

        file_info.append(file)
    return file_info


def make_dirs(file_info):
    for file in file_info:
        if os.path.exists(file[1]) is False:
            os.mkdir(file[1])


def move_files(file_info):
    for file in file_info:
        parsed_f = os.path.split(file[0])[1]
        if os.path.isfile(os.path.join(file[1], parsed_f)) is False:
            os.rename(file[0], os.path.join(file[1], parsed_f))


def edit_genres(file_info):
    for file in file_info:
        audio = FLAC(file[0])
        genres = audio.tags['genre']
        new_genres = genres
        for i in genres:
            i = str(i)
            matched = True

            match i.lower():
                case 'alternative':
                    pass
                case 'ambient':
                    pass
                case 'dance':
                    pass
                case 'electronic':
                    pass
                case 'funk':
                    pass
                case 'hip-hop':
                    pass
                case 'indie':
                    pass
                case 'jazz':
                    pass
                case 'master':
                    pass
                case 'metal':
                    pass
                case 'pop':
                    pass
                case 'psychedelia':
                    pass
                case 'punk':
                    pass
                case 'r&b':
                    pass
                case 'rap':
                    pass
                case 'rock':
                    pass
                case 'soul':
                    pass
                case _:
                    matched = False

            if matched is False:
                fixed = fix_genres(i)
                fixed[0] = new_genres[genres.index(i)]
                fixed.pop(0)
                for genre in fixed:
                    new_genres.append(genre)

        if new_genres != genres:
            audio.tags['genre'] = new_genres
            audio.save()


def fix_genres(genre):
    i = genre.lower()

    new_genre_list = []
    split_genres = []

    if '&' in i:
        split_genres = i.split('&')
        for x in split_genres:
            new_genre_list.append(x.strip())

    elif '/' in i:
        split_genres = i.split('/')

        for x in split_genres:
            new_genre_list.append(x.strip())

    elif 'Rock' in i:
        new_genre_list.append('Rock')

    elif 'Jazz' in i and i != 'Jazz':
        new_genre_list.append('Jazz')

    elif i == 'New Wave':
        new_genre_list.append('Rock')
        new_genre_list.append('Punk')

    elif 'Film' in i or 'Soundtrack' in i:
        new_genre_list.append('Miscellaneous')

    elif 'Musical Theatre' in i:
        new_genre_list.append('Miscellaneous')

    elif 'Latin' in i:
        new_genre_list.append('Miscellaneous')

    elif 'Children' in i:
        new_genre_list.append('Miscellaneous')

    elif 'Classical' in i:
        new_genre_list.append('Miscellaneous')

    else:
        inp = input("Couldn't match genre, Enter genre or nothing for Misc")
        parsed = inp.lower().capitalize()
        if inp != '':
            new_genre_list.append(parsed)

    return new_genre_list


def remove_empty_dir(dir):
    empty = [root for root, dirs, files, in os.walk(dir)
             if not len(dirs) and not len(files)]
    for folder in empty:
        os.rmdir(folder)


main()
