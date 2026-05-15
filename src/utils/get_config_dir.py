import os
import platform
from pathlib import Path
from typing import cast


def get_config_dir(app_name: str = "LuxDown") -> Path:
    if platform.system() == "Windows":
        config_dir = Path(cast(str, os.getenv("APPDATA"))) / app_name
    elif platform.system() == "Darwin":
        config_dir = Path.home() / "Library" / "Application Support" / app_name
    else:
        config_dir = Path.home() / ".config" / app_name
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir