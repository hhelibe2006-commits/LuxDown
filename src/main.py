"""
主函数入口模块
"""
import sys

# pylint: disable=no-name-in-module
from PySide6.QtGui import QIcon
# pylint: disable=no-name-in-module
from PySide6.QtWidgets import QApplication
from qt_material import apply_stylesheet

from src.ui import MainInterface
from src.utils.locale import load_translations


def main() -> None:
    """
    主函数
    进行主界面的创建与显示，并指定应用图标
    """
    app=QApplication(sys.argv)
    load_translations(app)
    apply_stylesheet(app, theme="dark_cyan.xml", extra = {'density_scale' : '0'})
    window=MainInterface()
    window.setWindowIcon(QIcon("LuxDown.png"))
    window.initialize()
    sys.exit(app.exec())

if __name__ == '__main__':
    """
    当该文件被直接运行时运行main()
    """
    main()
