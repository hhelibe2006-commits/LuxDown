from PySide6.QtCore import Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenuBar, QMainWindow, QMenu, QFileDialog, QMessageBox

from src.information import settings_manager
from src.widgets.message_box import MessageBox
from src.ui.settings_interface import SettingsInterface


class MenuBar(QMenuBar):
    def __init__(self, parent: QMainWindow) -> None:
        super().__init__(parent)
        self.settings_dialog: SettingsInterface = SettingsInterface(parent)
        settings_menu: QAction = self.addAction(self.tr("设置"))
        settings_menu.triggered.connect(self.on_settings)
        cookies_menu: QMenu = self.addMenu(self.tr("Cookie"))
        w: QAction = cookies_menu.addAction(self.tr("导入cookies"))
        d: QAction = cookies_menu.addAction(self.tr("清除cookies"))
        w.triggered.connect(self.import_cookies)
        d.triggered.connect(self.clear_cookies)

    @Slot()
    def clear_cookies(self) -> None:
        reply = MessageBox(
            self,
            title='确认',
            text='是否删除',
            buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.No:
            return
        settings_manager.clear_cookies()

    @Slot()
    def import_cookies(self) -> None:
        file, _ = QFileDialog.getOpenFileName(self)
        if file:
            settings_manager.import_cookies(file)

    @Slot()
    def on_settings(self) -> None:
        self.settings_dialog.exec()
        self.settings_dialog.synchronous()
