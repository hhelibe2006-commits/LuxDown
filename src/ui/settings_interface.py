"""
该文件存储设置界面类
"""
from typing import Callable

# pylint: disable=no-name-in-module
from PySide6.QtCore import Slot, QRunnable, QThreadPool
# pylint: disable=no-name-in-module
from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, \
    QPushButton, QFileDialog, QComboBox, QSizePolicy, QCheckBox, QMainWindow

from src.information import settings_manager
from src.utils import set_window_size, center_ui


class SettingsInterface(QDialog):
    """
    该类为设置界面类
    """
    def __init__(self, parent : QMainWindow = None) -> None:
        super().__init__(parent)
        self.vbox : QVBoxLayout = QVBoxLayout(self)
        self.path_input : QLineEdit = QLineEdit()
        self.audio_box : QCheckBox = QCheckBox(self.tr("音频"))
        self.video_box : QCheckBox = QCheckBox(self.tr("视频"))
        self.audio_combobox : QComboBox = QComboBox()
        self.video_combobox : QComboBox = QComboBox()
        self.language_combobox : QComboBox = QComboBox()
        self.path_button : QPushButton = QPushButton(self.tr("选择路径"))
        self.apply_button : QPushButton = QPushButton(self.tr("保存"))
        self.cancel_button : QPushButton = QPushButton(self.tr("取消"))
        self.initialize()

    def initialize(self) -> None:
        self._initialize_path()
        self._initialize_download_content()
        self._initialize_format()
        self._initialize_windows()
        self._initialize_buttons()

    def synchronous(self) -> None:
        self.path_input.setText(settings_manager.default_download_dir)

        self.audio_box.setChecked(settings_manager.download_audio)
        self.video_box.setChecked(settings_manager.download_video)

        self.audio_combobox.setCurrentText(settings_manager.current_audio_format)
        self.video_combobox.setCurrentText(settings_manager.current_video_format)

    def _initialize_buttons(self) -> None:
        self.apply_button.clicked.connect(self._on_apply_button)
        self.cancel_button.clicked.connect(self.close)
        hbox : QHBoxLayout = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.apply_button)
        hbox.addWidget(self.cancel_button)
        self.vbox.addLayout(hbox)

    def _initialize_windows(self) -> None:
        self.setWindowTitle(self.tr("设置"))
        set_window_size(self, ratio= 0.6)
        center_ui(self)
        self.vbox.addStretch()

    def _initialize_path(self) -> None:
        self.path_input.setPlaceholderText(self.tr("下载路径"))
        self.path_button.clicked.connect(self._choose_dir)
        self.path_input.setText(settings_manager.default_download_dir)
        hbox : QHBoxLayout = QHBoxLayout()
        hbox.addWidget(self.path_input)
        hbox.addWidget(self.path_button)
        self.vbox.addWidget(QLabel(self.tr("下载路径:")))
        self.vbox.addLayout(hbox)

    def _initialize_download_content(self) -> None:
        self.audio_box.setCheckable(True)
        self.video_box.setCheckable(True)
        self.audio_box.setChecked(settings_manager.download_audio)
        self.video_box.setChecked(settings_manager.download_video)
        hbox : QHBoxLayout = QHBoxLayout()
        hbox.addWidget(self.audio_box)
        hbox.addWidget(self.video_box)
        self.vbox.addWidget(QLabel(self.tr("下载内容:")))
        self.vbox.addLayout(hbox)

    def _initialize_format(self) -> None:
        self.audio_combobox.addItems(settings_manager.audio_formats)
        self.video_combobox.addItems(settings_manager.video_formats)
        self.audio_combobox.setCurrentText(settings_manager.current_audio_format)
        self.video_combobox.setCurrentText(settings_manager.current_video_format)
        self.audio_combobox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.video_combobox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.vbox.addWidget(QLabel(self.tr("格式选择")))
        hbox : QHBoxLayout = QHBoxLayout()
        hbox.addWidget(QLabel(self.tr("音频:")))
        hbox.addWidget(self.audio_combobox)
        hbox.addWidget(QLabel(self.tr("视频:")))
        hbox.addWidget(self.video_combobox)
        self.vbox.addLayout(hbox)

    @Slot()
    def _choose_dir(self) -> None:
        dir_path : str = QFileDialog.getExistingDirectory(self, self.tr("选择文件夹"), self.path_input.text())
        if dir_path:
            self.path_input.setText(dir_path)

    @Slot()
    def _on_apply_button(self) -> None:
        dict_settings : dict = {
            "path_input": self.path_input.text(),
            "audio": self.audio_combobox.currentText(),
            "video": self.video_combobox.currentText(),
            "on_audio": self.audio_box.isChecked(),
            "on_video": self.video_box.isChecked(),
        }
        revise : SettingsInterface.ReviseSettings = self.ReviseSettings(settings_manager.apply_settings, dict_settings)
        QThreadPool.globalInstance().start(revise)
        self.close()

    class ReviseSettings(QRunnable):
        def __init__(self, settings_info : Callable[[dict], None], data : dict) -> None:
            super().__init__()
            self.settings_info : Callable[[dict], None] = settings_info
            self.data : dict = data

        def run(self) -> None:
            self.settings_info(self.data)
