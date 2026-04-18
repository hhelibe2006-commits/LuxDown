from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QCheckBox, QVBoxLayout, QHBoxLayout, \
    QPushButton, QFileDialog, QGroupBox, QComboBox, QSizePolicy
from utils import set_window_size, center_ui

class SettingsInterface(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.path_input = QLineEdit()
        self.group_box1 = QGroupBox("音频")
        self.group_box2 = QGroupBox("视频")
        self.combo1 = QComboBox()
        self.combo2 = QComboBox()
        self.path_input.setPlaceholderText("下载路径")
        self.path_button = QPushButton("选择路径")
        self.path_button.clicked.connect(self.choos_dir)
        self.path_input.setText("C:\\Users\\hhhhh\\Downloads")
        self.initialize_ui()

    def initialize_ui(self):
        self.setWindowTitle("设置")
        self.group_box1.setCheckable(True)
        self.group_box2.setCheckable(True)
        self.combo1.addItems(["mp3"])
        self.combo2.addItems(["mp4"])
        self.combo1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.combo2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        set_window_size(self, 0.6)
        center_ui(self)
        hbox = QHBoxLayout()
        hbox.addWidget(self.path_input)
        hbox.addWidget(self.path_button)
        self.layout.addWidget(QLabel("下载路径:"))
        self.layout.addLayout(hbox)
        hbox = QHBoxLayout()
        hbox.addWidget(self.group_box1)
        hbox.addWidget(self.group_box2)
        self.layout.addWidget(QLabel("下载内容:"))
        self.layout.addLayout(hbox)
        self.layout.addWidget(QLabel("格式选择"))
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("音频:"))
        hbox.addWidget(self.combo1)
        hbox.addWidget(QLabel("视频:"))
        hbox.addWidget(self.combo2)
        self.layout.addLayout(hbox)
        self.layout.addStretch()

    def choos_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self,"选择文件夹", self.path_input.text())
        if dir_path:
            self.path_input.setText(dir_path)

