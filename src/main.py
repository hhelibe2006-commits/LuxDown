"""
朱函数入口模块
"""
import sys
# pylint: disable=no-name-in-module
from PySide6.QtGui import QIcon
# pylint: disable=no-name-in-module
from PySide6.QtWidgets import QApplication
from src.ui import MainInterface

def main():
    """
    主函数
    进行主界面的创建与显示，并指定应用图标
    """
    app=QApplication(sys.argv)
    windows=MainInterface()
    windows.setWindowIcon(QIcon("LuxDown.png"))
    windows.initialize()
    sys.exit(app.exec())

if __name__ == '__main__':
    """
    当该文件被直接运行时运行main()
    """
    main()
