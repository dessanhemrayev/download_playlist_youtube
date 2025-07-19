import os
import re
import logging
from urllib.parse import urlparse, parse_qs
from typing import List, Optional
from pytubefix import Playlist

# Настройка логгирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def sanitize_title(title: str) -> str:
    """Очистка названия плейлиста для использования в пути"""
    safe_title = re.sub(r'[<>:"/\\|?*\x00-\x1F]', "", title)
    safe_title = safe_title.strip()
    return safe_title or None  # Возвращает None, если строка пустая


def get_playlist_id(url: str) -> Optional[str]:
    """Извлечение ID плейлиста из URL"""
    try:
        parsed = urlparse(url)
        return parse_qs(parsed.query).get("list", [None])[0]
    except Exception as e:
        logger.warning(f"Не удалось извлечь ID плейлиста из {url}: {e}")
        return None


def get_download_directory(
    main_dir: str, playlist_title: str, playlist_url: str
) -> str:
    """Создание безопасного пути для сохранения плейлиста"""
    safe_title = sanitize_title(playlist_title)

    if not safe_title:
        playlist_id = get_playlist_id(playlist_url)
        safe_title = f"playlist_{playlist_id}" if playlist_id else "unnamed_playlist"
        logger.warning(f"Используется резервное имя директории: {safe_title}")

    download_dir = os.path.join(main_dir, "youtube", safe_title)
    os.makedirs(download_dir, exist_ok=True)
    return download_dir


def download_playlist_videos(playlist: Playlist, download_dir: str) -> None:
    """Загрузка видео из плейлиста с обработкой ошибок"""
    for video in playlist.videos:
        try:
            logger.info(f"downloading : {video.title} with url : {video.watch_url}")
            ys = video.streams.get_highest_resolution()
            if ys is None:
                logger.warning(f"No stream found for video: {video.title}")
                continue
            ys.download(output_path=download_dir)
        except Exception as e:
            logger.exception(f"Неожиданная ошибка при обработке {video}: {e}")


def youtube_playlists_download(main_directory: str, playlists: List[str]) -> str:
    """
    Загружает все видео из указанных плейлистов YouTube

    Args:
        main_directory: Базовая директория для сохранения видео
        playlists: Список URL-адресов плейлистов

    Returns:
        Сообщение о завершении загрузки
    """
    if not playlists:
        logger.info("Список плейлистов пуст")
        return "Нет плейлистов для загрузки"

    for playlist_url in playlists:
        try:
            logger.info(f"Обработка плейлиста: {playlist_url}")
            playlist = Playlist(playlist_url)

            # Явно загружаем видео для получения метаданных
            _ = playlist.videos

            download_dir = get_download_directory(
                main_directory, playlist.title, playlist_url
            )

            logger.info(
                f"Найдено видео в плейлисте '{playlist.title}': {len(playlist.video_urls)}"
            )
            download_playlist_videos(playlist, download_dir)

        except Exception as e:
            logger.exception(
                f"Неожиданная ошибка при обработке плейлиста {playlist_url}: {e}"
            )

    return "Загрузка завершена успешно"


if __name__ == "__main__":
    youtube_playlists = []
    home_directory = input("Укажите путь к вашей домашней директории:")
    # Validate directory
    if not os.path.exists(home_directory):
        logger.error(f"Directory does not exist: {home_directory}")
        exit(1)
    if not os.path.isdir(home_directory):
        logger.error(f"Path is not a directory: {home_directory}")
        exit(1)

    playlist_url = input("Укажите ссылку на playlist:")

    # Validate playlist URL format
    if playlist_url and "list=" not in playlist_url:
        logger.error(
            "Invalid playlist URL format. URL should contain 'list=' parameter."
        )
        exit(1)

    youtube_playlists.append(playlist_url)
    result = youtube_playlists_download(home_directory, youtube_playlists)
    logger.info(result)
