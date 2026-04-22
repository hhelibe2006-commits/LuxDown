"""
该文件存放调用yt-dlp进行解析的函数与类
"""
from typing import Any
from yt_dlp import YoutubeDL
def parse(url):
    with YoutubeDL() as ydl:
        info:Any = ydl.extract_info(url, download=False)
        if not info:
            return []
        clist = [
            'title', 'id', 'description', 'ext', 'duration_string',
            'filesize_approx', 'webpage_url'
        ]
        llist = []
        if info.get('_type') is not None:
            for i in info.get('entries'):
                llist.append({j:k for j,k in i.items() if j in clist})
        else:
            llist.append({j:k for j,k in info.items() if j in clist})
        return llist,info.get('title'),info.get('thumbnail')
