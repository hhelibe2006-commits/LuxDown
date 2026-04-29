"""
该文件存放调用yt-dlp进行下载的函数与类
"""
import yt_dlp


def download(url, progress_hook, index, settings):
    ydl_opts = {
        "outtmpl": f"{settings.path_input}\\{index}-%(title)s.%(ext)s",
        'progress_hooks': [progress_hook],
        'max_sleep_interval': 30,
        #'quiet': True,
        #'no_color': True,
    }
    if settings.on_audio and settings.on_video:
        ydl_opts['format'] = 'bestvideo+bestaudio/best'
        ydl_opts['merge_output_format'] = settings.video1

    elif settings.on_audio:
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['merge_output_format'] = settings.audio1
    elif settings.on_video:
        ydl_opts['format'] = 'bestvideo'
        ydl_opts['merge_output_format'] = settings.video1
    else:
        ydl_opts['format'] = ''

    with yt_dlp.YoutubeDL(ydl_opts) as ydl: # type: ignore
        ydl.download([url])
