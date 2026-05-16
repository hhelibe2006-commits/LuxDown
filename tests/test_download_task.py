import pytest
from types import SimpleNamespace

from src import DownloadTask


class DummyLogger:
    def __init__(self):
        self.messages = []

    def error(self, msg):
        self.messages.append(('error', str(msg)))

    def info(self, msg):
        self.messages.append(('info', str(msg)))


def test_download_task_success(monkeypatch):
    # Arrange: monkeypatch the download implementation used by DownloadTask
    def fake_download(url, progress_hook, index, settings, logger, resolution):
        # simulate a progress callback invocation
        progress_hook({'status': 'downloading', 'percent': 50})
        return True

    monkeypatch.setattr('src.core.download_task.download', fake_download)

    settings = SimpleNamespace(
        default_download_dir='.',
        cookies_file='cookies.txt',
        download_audio=True,
        download_video=True,
        current_video_format='mp4',
        current_audio_format='mp3'
    )
    logger = DummyLogger()
    called = {}

    def finished_cb(success, index):
        called['finished'] = (success, index)

    task = DownloadTask('http://example.com', 1, settings, logger, '1920x1080', progress_callback=lambda d: None, finished_callback=finished_cb)

    # Act
    res = task.run()

    # Assert
    assert res is True
    assert called.get('finished') == (True, 1)


def test_download_task_cancelled(monkeypatch):
    # Arrange: fake download that invokes progress_hook (which will raise due to cancel)
    def fake_download(url, progress_hook, index, settings, logger, resolution):
        # progress hook will be called and (if task was cancelled) raise DownloadCancelled
        progress_hook({'status': 'downloading'})
        return True

    monkeypatch.setattr('src.core.download_task.download', fake_download)

    settings = SimpleNamespace(
        default_download_dir='.',
        cookies_file='cookies.txt',
        download_audio=True,
        download_video=True,
        current_video_format='mp4',
        current_audio_format='mp3'
    )
    logger = DummyLogger()
    called = {}

    def finished_cb(success, index):
        called['finished'] = (success, index)

    task = DownloadTask('http://example.com', 2, settings, logger, '1920x1080', progress_callback=lambda d: None, finished_callback=finished_cb)

    # Cancel before running so the progress wrapper will raise DownloadCancelled
    task.cancel()
    res = task.run()

    assert res is False
    assert called.get('finished') == (False, 2)