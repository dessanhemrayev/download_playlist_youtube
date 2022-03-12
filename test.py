import re
from pytube import Playlist
playlist = Playlist('https://youtube.com/playlist?list=PLVU8__p4xuHIA71maXPilcM5791EEjgSB')   
DOWNLOAD_DIR = '/home/dessan/youtube'
playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)") 
print(playlist)