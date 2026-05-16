from types import SimpleNamespace

from src import build_ydl_opts


def test_build_ydl_opts_minimal(tmp_path):
    settings = SimpleNamespace(
        default_download_dir=str(tmp_path),
        cookies_file=str(tmp_path / "cookies.txt"),
        download_audio=True,
        download_video=True,
        current_video_format='mp4',
        current_audio_format='mp3',
    )
    # logger is not used by build_ydl_opts at runtime; pass None or a dummy
    opts = build_ydl_opts(settings, logger=None, index=1, resolution='1920x1080', progress_hook=lambda d: None)
    assert isinstance(opts, dict)
    assert 'outtmpl' in opts
    # outtmpl should include the configured download dir
    assert str(tmp_path) in opts['outtmpl']
    assert 'progress_hooks' in opts and isinstance(opts['progress_hooks'], list)