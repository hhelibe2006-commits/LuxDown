"""
该文件存放调用yt-dlp进行解析的函数与类
"""
from yt_dlp import YoutubeDL


def extract_info(url):
    ydl_opts = {
        'max_sleep_interval': 30,
                }
    with YoutubeDL(ydl_opts) as ydl: # type: ignore
        info = ydl.extract_info(url, download=False)
        if not info:
            return []
        desired_keys = [
            'title', 'id', 'description', 'ext', 'duration_string',
            'filesize_approx', 'webpage_url'
        ]
        entries = []
        if info.get('_type') is not None:
            for entry in info.get('entries'):
                entries.append({key:value for key,value in entry.items() if key in desired_keys})
        else:
            entries.append({j:k for j,k in info.items() if j in desired_keys})
        return entries,info.get("description"), info.get('title'), info.get('thumbnail')
