"""
该文件存放调用yt-dlp进行下载的函数与类
"""
import yt_dlp
def download(url, hook):
    ydl_opts = {
        "outtmpl": "C:\\Users\\hhhhh\\Downloads\\%(title)s.%(ext)",
        'progress_hooks': [hook]}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
