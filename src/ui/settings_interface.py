from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, \
    QPushButton, QFileDialog, QGroupBox, QComboBox, QSizePolicy
from PySide6.QtCore import Slot
from utils import set_window_size, center_ui

class SettingsInterface(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vbox = QVBoxLayout(self)
        self.path_input = QLineEdit()
        self.audio_box = QGroupBox("音频")
        self.video_box = QGroupBox("视频")
        self.audio_combobox = QComboBox()
        self.video_combobox = QComboBox()
        self.path_button = QPushButton("选择路径")
        self.initialize()

    def initialize(self):
        self.initialize_path()
        self.initialize_download_content()
        self.initialize_format()
        self.initialize_windows()

    def initialize_windows(self):
        self.setWindowTitle("设置")
        set_window_size(self, percentage = 0.6)
        center_ui(self)
        self.vbox.addStretch()

    def initialize_path(self):
        self.path_input.setPlaceholderText("下载路径")
        self.path_button.clicked.connect(self.choose_dir)
        self.path_input.setText("C:\\Users\\hhhhh\\Downloads")
        hbox = QHBoxLayout()
        hbox.addWidget(self.path_input)
        hbox.addWidget(self.path_button)
        self.vbox.addWidget(QLabel("下载路径:"))
        self.vbox.addLayout(hbox)

    def initialize_download_content(self):
        self.audio_box.setCheckable(True)
        self.video_box.setCheckable(True)
        hbox = QHBoxLayout()
        hbox.addWidget(self.audio_box)
        hbox.addWidget(self.video_box)
        self.vbox.addWidget(QLabel("下载内容:"))
        self.vbox.addLayout(hbox)

    def initialize_format(self):
        self.audio_combobox.addItems(["mp3"])
        self.video_combobox.addItems(["mp4"])
        self.audio_combobox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.video_combobox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.vbox.addWidget(QLabel("格式选择"))
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("音频:"))
        hbox.addWidget(self.audio_combobox)
        hbox.addWidget(QLabel("视频:"))
        hbox.addWidget(self.video_combobox)
        self.vbox.addLayout(hbox)

    @Slot()
    def choose_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "选择文件夹", self.path_input.text())
        if dir_path:
            self.path_input.setText(dir_path)

