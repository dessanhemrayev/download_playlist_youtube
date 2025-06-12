import os
from pytube import Playlist, YouTube

def youtube_playlists_download(main_directory, playlists):
    """
    Загружает все видео из указанных плейлистов YouTube в указанную директорию.

    :param main_directory: Базовая директория для сохранения видео.
    :param playlists: Список URL-адресов плейлистов.
    :return: Сообщение о завершении загрузки.
    """
    for playlist_url in playlists:
        try:
            playlist = Playlist(playlist_url)
            # Очистка названия плейлиста для безопасного использования в пути
            safe_title = "".join(c for c in playlist.title if c.isalnum() or c in (' ', '-', '_')).strip()
            download_dir = os.path.join(main_directory, 'youtube', safe_title)
            os.makedirs(download_dir, exist_ok=True)

            print(f"Найдено видео в плейлисте '{playlist.title}': {len(playlist.video_urls)}")

            for video_url in playlist.video_urls:
                try:
                    yt = YouTube(video_url)
                    print(f"Загрузка: {yt.title} ({video_url})")

                    stream = (
                        yt.streams
                        .filter(progressive=True, file_extension='mp4')
                        .order_by('resolution')
                        .desc()
                        .first()
                    )

                    if not stream:
                        print(f"Не найден подходящий стрим для видео: {yt.title}")
                        continue

                    stream.download(output_path=download_dir)
                except Exception as e:
                    print(f"Ошибка при обработке видео {video_url}: {e}")

        except Exception as e:
            print(f"Ошибка при обработке плейлиста {playlist_url}: {e}")

    return "Загрузка завершена успешно"

if __name__ == "__main__":
    # Пример использования
    youtube_playlists = [
        "https://www.youtube.com/playlist?list=PLirAqAtl_h2pDdp4fxwJcENJ1xV5yZYZq"
    ]
    MAIN_DIRECTORY = "/home/user"  # Укажите путь к вашей домашней директории 
    result = youtube_playlists_download(MAIN_DIRECTORY, youtube_playlists)
    print(result)
