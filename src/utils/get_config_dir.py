"""
该函数根据操作系统返回一个适合存储应用程序配置文件的目录路径。
它会检查当前操作系统，并根据不同的系统返回相应的路径。
在Windows上，它使用APPDATA环境变量；
在macOS上，它使用用户的Library/Application Support目录；
在其他系统（如Linux）上，它使用用户的.home/config目录。
最后，它确保该目录存在，如果不存在则创建它，并返回该目录的路径。
"""

import os
import platform
from pathlib import Path
from typing import cast


def get_config_dir(app_name: str = "LuxDown") -> Path:
    if platform.system() == "Windows":
        config_dir: Path = Path(cast(str, os.getenv("APPDATA"))) / app_name
    elif platform.system() == "Darwin":
        config_dir: Path = Path.home() / "Library" / "Application Support" / app_name
    else:
        config_dir: Path = Path.home() / ".config" / app_name
    # 确保目录存在，如果不存在则创建
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir
