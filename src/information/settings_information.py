import json
from pathlib import Path
class SettingsInformation:
    def __init__(self):
        self.path_input = str(Path.home()/"Downloads")
        self.audio = ["mp3", "m4a", "acc", "wav", "ogg", "flac"]
        self.video = ["mp4", "webm", "mov", "mkv"]
        self.audio1 = "mp3"
        self.video1 = "mp4"
        self.on_audio = True
        self.on_video = True
        self.data="settings.json"
        self.initialize()

    def initialize(self):
        if Path(self.data).exists():
            with open(self.data, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data.get("path_input") is not None:
                    self.path_input = data.get("path_input")
                else:
                    pass
                if data.get("audio") is not None and data.get("audio") in self.audio:
                    self.audio1 = data.get("audio")
                else:
                    pass
                if data.get("video") is not None and data.get("video") in self.video:
                    self.video1 = data.get("video")
                else:
                    pass
                if data.get("on_audio") is not None and data.get("on_audio") in {True, False}:
                    self.on_audio = data.get("on_audio")
                else:
                    pass
                if data.get("on_video") is not None and data.get("on_video") in {True, False}:
                    self.on_video = data.get("on_video")
                else:
                    pass
        else:
            self.__initialize_json()

    def __initialize_json(self):
        data = {
            "path_input" : self.path_input,
            "audio" : self.audio1,
            "video" : self.video1,
            "on_audio" : self.on_audio,
            "on_video" : self.on_video,
        }
        with open(self.data, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def revise_settings(self, settings : dict):
        if settings.get("path_input") is not None:
            self.path_input = settings.get("path_input")
        else:
            pass
        if settings.get("audio") is not None and settings.get("audio") in self.audio:
            self.audio1 = settings.get("audio")
        else:
            pass
        if settings.get("video") is not None and settings.get("video") in self.video:
            self.video1 = settings.get("video")
        else:
            pass
        if settings.get("on_audio") is not None and settings.get("on_audio") in {True, False}:
            self.on_audio = settings.get("on_audio")
        else:
            pass
        if settings.get("on_video") is not None and settings.get("on_video") in {True, False}:
            self.on_video = settings.get("on_video")
        else:
            pass
        with open(self.data, "w", encoding="utf-8") as f:
            json.dump(settings, f, ensure_ascii=False, indent=4)
