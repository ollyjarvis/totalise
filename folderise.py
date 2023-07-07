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
        artist = audio["ARTIST"][0].replace('/', '_').replace('\\' , '_').strip()
        new_dir = os.path.join(music_dir, artist)
        
        if os.path.exists(new_dir) == False:
            os.mkdir(new_dir)
            print("Directory '% s' created" % new_dir)
            
        if os.path.isfile(os.path.join(new_dir, parsed_f)) == False:
            os.rename(f, os.path.join(new_dir, parsed_f))
            count += 1
        else:
            print("Skipped ", parsed_f, " \nFile of same name in output folder !")

print("Finished moved ", count, " files")
