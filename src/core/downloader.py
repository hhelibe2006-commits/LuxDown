"""
该文件存放调用yt-dlp进行下载的函数与类
"""
import yt_dlp


def download(url, progress_hook, index, settings):
    ydl_opts = {
        "outtmpl": f"{settings.default_download_dir}\\{index}-%(title)s.%(ext)s",
        'progress_hooks': [progress_hook],
        'max_sleep_interval': 30,
        'external_downloader': 'aria2c',
        'external_downloader_args': [
            '--min-split-size=1M',
            '--max-connection-per-server=16',
            '--split=16',
            '--max-overall-download-limit=0'
        ],
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
        ydl_opts['format'] = ''

    with yt_dlp.YoutubeDL(ydl_opts) as ydl: # type: ignore
        ydl.download([url])
