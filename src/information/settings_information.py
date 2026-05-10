"""
该文件存放调用json进行设置存储的函数与类
"""
import json
from typing import cast
from pathlib import Path

class SettingsManager:
    """
    该类用于设置文件的创建与改查
    """
    def __init__(self) -> None:
        self.default_download_dir : str = str(Path.home() / "Downloads")
        self.audio : list = ["mp3", "m4a", "aac", "wav", "ogg", "flac"]
        self.video : list = ["mp4", "webm", "mov", "mkv"]
        self.current_audio_format : str = "mp3"
        self.current_video_format : str = "mp4"
        self.download_audio : bool = True
        self.download_video : bool = True
        self.settings_file : str = "settings.json"
        self.load_from_file()

    def load_from_file(self) -> None:
        if Path(self.settings_file).exists():
            with open(self.settings_file, "r", encoding="utf-8") as f:
                data : dict = json.load(f)
                self._update_from_dict(data)
        else:
            self._create_default_config()

    def _create_default_config(self) -> None:
        data : dict = {
            "path_input" : self.default_download_dir,
            "audio" : self.current_audio_format,
            "video" : self.current_video_format,
            "on_audio" : self.download_audio,
            "on_video" : self.download_video,
        }
        with open(self.settings_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def apply_settings(self, settings : dict) -> None:
        self._update_from_dict(settings)
        with open(self.settings_file, "w", encoding="utf-8") as f:
            json.dump(settings, f, ensure_ascii=False, indent=4)

    def _update_from_dict(self,settings : dict) -> None:
        if isinstance(settings.get("path_input"), str):
            self.default_download_dir = cast(str, settings.get("path_input"))

        if isinstance(settings.get("audio"), str) and settings.get("audio") in self.audio:
            self.current_audio_format = cast(str, settings.get("audio"))

        if isinstance(settings.get("video"), str) and settings.get("video") in self.video:
            self.current_video_format = cast(str, settings.get("video"))

        if isinstance(settings.get("on_audio"), bool):
            self.download_audio = cast(bool, settings.get("on_audio"))

        if isinstance(settings.get("on_video"), bool):
            self.download_video = cast(bool, settings.get("on_video"))
