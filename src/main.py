import sys
from PySide6.QtWidgets import QApplication
from ui import MainInterface

def main():
    app=QApplication(sys.argv)
    windows=MainInterface()
    windows.initialize()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()