"""
该文件存放调用json进行设置存储的函数与类
"""
import json
from http import cookiejar
from pathlib import Path
from typing import Any, cast

from src.utils import get_config_dir


class SettingsManager:
    """
    该类用于设置文件的创建与改查
    """
    audio_formats : list = ["mp3", "m4a", "aac", "wav", "ogg", "flac"]
    video_formats : list = ["mp4", "webm", "mov", "mkv"]
    def __init__(self) -> None:
        self.default_download_dir : str = str(Path.home() / "Downloads")
        self.current_audio_format : str = "mp3"
        self.current_video_format : str = "mp4"
        self.download_audio : bool = True
        self.download_video : bool = True
        self.settings_file : str = str(get_config_dir() / "settings.json")
        self.cookies_file : str = str(get_config_dir() / "cookies.txt")
        self.load_from_file()

    def load_from_file(self) -> None:
        if Path(self.settings_file).exists():
            with open(self.settings_file, "r", encoding="utf-8") as f:
                data : dict = json.load(f)
                self._update_from_dict(data)
        else:
            self._create_default_config()

        if not Path(self.cookies_file).exists():
            cj = cookiejar.MozillaCookieJar(self.cookies_file)
            cj.save(ignore_discard=True, ignore_expires=True)

    def _create_default_config(self) -> None:
        data : dict = {
            "download_dir" : self.default_download_dir,
            "audio_format" : self.current_audio_format,
            "video_format" : self.current_video_format,
            "enable_audio" : self.download_audio,
            "enable_video" : self.download_video,
        }
        with open(self.settings_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def apply_settings(self, settings : dict[str,Any]) -> None:
        self._update_from_dict(settings)
        new_settings : dict[str,Any] = self.as_dict()
        with open(self.settings_file, "w", encoding="utf-8") as f:
            json.dump(new_settings, f, ensure_ascii=False, indent=4)

    def as_dict(self):
        return {
            "download_dir" : self.default_download_dir,
            "audio_format" : self.current_audio_format,
            "video_format" : self.current_video_format,
            "enable_audio" : self.download_audio,
            "enable_video" : self.download_video,
        }
    def _update_from_dict(self,settings : dict) -> None:
        if isinstance(settings.get("download_dir"), str):
            self.default_download_dir = cast(str, settings.get("download_dir"))

        if isinstance(settings.get("audio_format"), str) and settings.get("audio_format") in self.audio_formats:
            self.current_audio_format = cast(str, settings.get("audio_format"))

        if isinstance(settings.get("video_format"), str) and settings.get("video_format") in self.video_formats:
            self.current_video_format = cast(str, settings.get("video_format"))

        if isinstance(settings.get("enable_audio"), bool):
            self.download_audio = cast(bool, settings.get("enable_audio"))

        if isinstance(settings.get("enable_video"), bool):
            self.download_video = cast(bool, settings.get("enable_video"))

settings_manager : SettingsManager = SettingsManager()