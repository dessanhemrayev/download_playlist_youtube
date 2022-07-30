import re
from pytube import Playlist

def youtube_playlists_download(main_directory,playlists):
    for playlist in playlists:
        playlist = Playlist(playlist)   
        DOWNLOAD_DIR = main_directory + '/youtube/'+playlist.title
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
    return 'Good lik'

if __name__ == "__main__":
    youtube_playlists=[]
    MAIN_DIRECTORY = '/home'
    youtube_playlists_download(MAIN_DIRECTORY,youtube_playlists)