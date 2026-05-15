"""
该文件存放调用yt-dlp进行解析的函数与类
"""
import os
import platform
from typing import Any

from yt_dlp import YoutubeDL

from signal import MyLogger


def extract_info(url : str, logger : MyLogger, cookies : str)\
        -> tuple[Any] | tuple[list[Any], str | None, str | None, str | None]:
    ydl_opts : dict = {
        'logger': logger,
        'max_sleep_interval': 30,
        'cookiefile': cookies,
                }
    if platform.system() == 'Windows':
        ydl_opts['deno_path'] = os.path.join('deno', 'deno.exe')

    with YoutubeDL(ydl_opts) as ydl: # type: ignore
        info = ydl.extract_info(url, download=False)
        if not info:
            return tuple()
        desired_keys : list = [
            'title', 'id', 'description', 'ext', 'duration_string',
            'filesize_approx', 'webpage_url', 'formats'
        ]
        entries = []
        if info.get('_type') is not None:
            for entry in info.get('entries'):
                entries.append({key: value for key,value in entry.items() if key in desired_keys})
        else:
            entries.append({key: info[key] for key in desired_keys if key in info})
        return entries, info.get("description"), info.get('title'), info.get('thumbnail')
