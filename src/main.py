"""
朱函数入口模块
"""
import sys

from PySide6.QtCore import QTranslator
# pylint: disable=no-name-in-module
from PySide6.QtGui import QIcon
# pylint: disable=no-name-in-module
from PySide6.QtWidgets import QApplication
from qt_material import apply_stylesheet

from src.ui import MainInterface


def main() -> None:
    """
    主函数
    进行主界面的创建与显示，并指定应用图标
    """
    app=QApplication(sys.argv)
    translator = QTranslator()
    #if translator.load("zh_CN.qm"):
    #    app.installTranslator( translator)
    apply_stylesheet(app, theme="dark_cyan.xml", extra = {'density_scale' : '0'})
    windows=MainInterface()
    windows.setWindowIcon(QIcon("LuxDown.png"))
    windows.initialize()
    sys.exit(app.exec())

if __name__ == '__main__':
    """
    当该文件被直接运行时运行main()
    """
    main()
