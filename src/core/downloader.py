"""
该文件存放调用yt-dlp进行下载的函数与类
"""
import os
import platform

import yt_dlp


def download(url, progress_hook, index, settings, logger):
    ydl_opts = {
        "logger": logger,
        "outtmpl": f'{os.path.join(settings.default_download_dir, f"{index}-%(title)s.%(ext)s")}',
        'progress_hooks': [progress_hook],
        'max_sleep_interval': 5,
        'socket_timeout': 30,
        'retries': 10,
        'fragment_retries': 3,
        'cookiefile': 'cookies.txt',
    }
    if settings.download_audio and settings.download_video:
        ydl_opts['format'] = 'bestvideo+bestaudio/best'
        ydl_opts['merge_output_format'] = settings.current_video_format

    elif settings.download_audio:
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['merge_output_format'] = settings.current_audio_format
    elif settings.download_video:
        ydl_opts['format'] = 'bestvideo'
        ydl_opts['merge_output_format'] = settings.current_video_format
    else:
        return False

    if platform.system() == 'Windows':
        ydl_opts['ffmpeg_location'] = os.path.join('ffmpeg', 'bin', 'ffmpeg.exe')
        ydl_opts['deno_path'] = os.path.join('deno', 'deno.exe')

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # type: ignore
        try:
            ydl.download([url])
        except Exception as e:
            raise e
    return True
