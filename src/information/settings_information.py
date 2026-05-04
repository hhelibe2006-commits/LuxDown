"""
该文件存放调用json进行设置存储的函数与类
"""
import json
from pathlib import Path

class SettingsManager:
    """
    该类用于设置文件的创建与改查
    """
    def __init__(self):
        self.default_download_dir = str(Path.home() / "Downloads")
        self.audio = ["mp3", "m4a", "aac", "wav", "ogg", "flac"]
        self.video = ["mp4", "webm", "mov", "mkv"]
        self.current_audio_format = "mp3"
        self.current_video_format = "mp4"
        self.download_audio = True
        self.download_video = True
        self.settings_file= "settings.json"
        self.load_from_file()

    def load_from_file(self):
        if Path(self.settings_file).exists():
            with open(self.settings_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self._update_from_dict(data)
        else:
            self._create_default_config()

    def _create_default_config(self):
        data = {
            "path_input" : self.default_download_dir,
            "audio" : self.current_audio_format,
            "video" : self.current_video_format,
            "on_audio" : self.download_audio,
            "on_video" : self.download_video,
        }
        with open(self.settings_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def apply_settings(self, settings : dict):
        self._update_from_dict(settings)
        with open(self.settings_file, "w", encoding="utf-8") as f:
            json.dump(settings, f, ensure_ascii=False, indent=4)

    def _update_from_dict(self,settings):
        if settings.get("path_input") is not None:
            self.default_download_dir = settings.get("path_input")
        else:
            pass
        if settings.get("audio") is not None and settings.get("audio") in self.audio:
            self.current_audio_format = settings.get("audio")
        else:
            pass
        if settings.get("video") is not None and settings.get("video") in self.video:
            self.current_video_format = settings.get("video")
        else:
            pass
        if settings.get("on_audio") is not None and settings.get("on_audio") in {True, False}:
            self.download_audio = settings.get("on_audio")
        else:
            pass
        if settings.get("on_video") is not None and settings.get("on_video") in {True, False}:
            self.download_video = settings.get("on_video")
        else:
            pass
