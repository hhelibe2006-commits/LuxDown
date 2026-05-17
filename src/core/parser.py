"""
该文件存放调用yt-dlp进行解析的函数与类
"""
import os
import platform
from typing import Any, Dict, List, Optional, Tuple

from yt_dlp import YoutubeDL

from src.signal import Logger


def extract_info(url: str, logger: Logger, cookies_file: str)\
        -> Tuple[List[Dict[str, Any]], Optional[str], Optional[str], Optional[str]]:
    """
    解析函数，将链接解析并返回元组
    """
    ydl_opts: dict = {
        'logger': logger,
        'max_sleep_interval': 30,
        'cookiefile': cookies_file,
    }
    if platform.system() == 'Windows':
        ydl_opts['deno_path'] = os.path.join('deno', 'deno.exe')

    elif platform.system() == 'Darwin':
        ydl_opts['deno_path'] = os.path.join('deno', 'deno.app')

    with YoutubeDL(ydl_opts) as ydl:  # type: ignore
        info = ydl.extract_info(url, download=False)
        if not info:
            return [], None, None, None

        desired_keys: List[str] = [
            'title', 'id', 'description', 'ext', 'duration_string',
            'filesize_approx', 'webpage_url', 'formats'
        ]

        entries: List[Dict[str, Any]] = []
        # 如果是 playlist / 多条目
        if info.get('_type') == 'playlist' or info.get('entries'):
            for entry in info.get('entries') or []:
                entries.append({key: value for key, value in (entry or {}).items() if key in desired_keys})
        else:
            entries.append({key: info[key] for key in desired_keys if key in info})

        return entries, info.get('description'), info.get('title'), info.get('thumbnail')
