"""
该文件存储设置界面类
"""
# pylint: disable=no-name-in-module
from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, \
    QPushButton, QFileDialog, QGroupBox, QComboBox, QSizePolicy, QCheckBox
# pylint: disable=no-name-in-module
from PySide6.QtCore import Slot, QRunnable, QThreadPool
from src.utils import set_window_size, center_ui
from src.information import SettingsManager

class SettingsInterface(QDialog):
    """
    该类为设置界面类
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vbox = QVBoxLayout(self)
        self.path_input = QLineEdit()
        self.audio_box = QCheckBox("音频")
        self.video_box = QCheckBox("视频")
        self.audio_combobox = QComboBox()
        self.video_combobox = QComboBox()
        self.path_button = QPushButton("选择路径")
        self.apply_button = QPushButton("保存")
        self.cancel_button = QPushButton("取消")
        self.settings_information = SettingsManager()
        self.initialize()

    def initialize(self):
        self.__initialize_path()
        self.__initialize_download_content()
        self.__initialize_format()
        self.__initialize_windows()
        self.__initialize_buttons()

    def synchronous(self):
        self.path_input.setText(self.settings_information.default_download_dir)

        self.audio_box.setChecked(self.settings_information.download_audio)
        self.video_box.setChecked(self.settings_information.download_video)

        self.audio_combobox.setCurrentText(self.settings_information.current_audio_format)
        self.video_combobox.setCurrentText(self.settings_information.current_video_format)

    def __initialize_buttons(self):
        self.apply_button.clicked.connect(self.__on_apply_button)
        self.cancel_button.clicked.connect(self.close)
        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.apply_button)
        hbox.addWidget(self.cancel_button)
        self.vbox.addLayout(hbox)

    def __initialize_windows(self):
        self.setWindowTitle("设置")
        set_window_size(self, ratio= 0.6)
        center_ui(self)
        self.vbox.addStretch()

    def __initialize_path(self):
        self.path_input.setPlaceholderText("下载路径")
        self.path_button.clicked.connect(self.__choose_dir)
        self.path_input.setText(self.settings_information.default_download_dir)
        hbox = QHBoxLayout()
        hbox.addWidget(self.path_input)
        hbox.addWidget(self.path_button)
        self.vbox.addWidget(QLabel("下载路径:"))
        self.vbox.addLayout(hbox)

    def __initialize_download_content(self):
        self.audio_box.setCheckable(True)
        self.video_box.setCheckable(True)
        self.audio_box.setChecked(self.settings_information.download_audio)
        self.video_box.setChecked(self.settings_information.download_video)
        hbox = QHBoxLayout()
        hbox.addWidget(self.audio_box)
        hbox.addWidget(self.video_box)
        self.vbox.addWidget(QLabel("下载内容:"))
        self.vbox.addLayout(hbox)

    def __initialize_format(self):
        self.audio_combobox.addItems(self.settings_information.audio)
        self.video_combobox.addItems(self.settings_information.video)
        self.audio_combobox.setCurrentText(self.settings_information.current_audio_format)
        self.video_combobox.setCurrentText(self.settings_information.current_video_format)
        self.audio_combobox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.video_combobox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.vbox.addWidget(QLabel("格式选择"))
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("音频:"))
        hbox.addWidget(self.audio_combobox)
        hbox.addWidget(QLabel("视频:"))
        hbox.addWidget(self.video_combobox)
        self.vbox.addLayout(hbox)

    @Slot()
    def __choose_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "选择文件夹", self.path_input.text())
        if dir_path:
            self.path_input.setText(dir_path)

    @Slot()
    def __on_apply_button(self):
        dict_settings = {
            "path_input": self.path_input.text(),
            "audio": self.audio_combobox.currentText(),
            "video": self.video_combobox.currentText(),
            "on_audio": self.audio_box.isChecked(),
            "on_video": self.video_box.isChecked(),
        }
        revise=self.ReviseSettings(self.settings_information.apply_settings, dict_settings)
        QThreadPool.globalInstance().start(revise)
        self.close()

    class ReviseSettings(QRunnable):
        def __init__(self, settings_info, data):
            super().__init__()
            self.settings_info = settings_info
            self.data = data

        def run(self):
            self.settings_info(self.data)
