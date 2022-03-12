import re
from pytube import Playlist

playlists=['https://youtube.com/playlist?list=PLR4wcBxrUGPAmndrGEiN0wiaFqG-L5Yd-','https://youtube.com/playlist?list=PLawfWYMUziZqyUL5QDLVbe3j5BKWj42E5','https://youtube.com/playlist?list=PLmRNNqEA7JoN2bp1VXDZcwVgKkiI94Oha'
            ]
name_directory=[]

for playlist in playlists:
    playlist = Playlist(playlist)   
    DOWNLOAD_DIR = '/home/dessan/youtube/'+playlist.title
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")    
    print(len(playlist.video_urls))    
    for url in playlist.video_urls:
        print(f"****{url.title} **** {url} ***")    
    for video in playlist.videos:
        print('downloading : {} with url : {}'.format(video.title, video.watch_url))
        video.streams.\
            filter(type='video', progressive=True, file_extension='mp4').\
            order_by('resolution').\
            desc().\
            first().\
            download(DOWNLOAD_DIR)