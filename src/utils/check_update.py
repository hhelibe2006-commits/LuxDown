VERSION="v0.1.0"
from PySide6.QtCore import Slot
import requests
from packaging import version
from PySide6.QtWidgets import QMessageBox

@Slot()
def check_update():
    api_url="https://api.github.com/repos/hhelibe2006-commits/LuxDown/releases/latest"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        latest_version = data['tag_name']
        download_url = data['html_url']
        if version.parse(latest_version) > version.parse(VERSION):
            reply = QMessageBox()
            reply.setWindowTitle('有新版本')
            reply.setText('是否下载')
            reply.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            an = reply.exec()
            if an == QMessageBox.StandardButton.Ok:
                from PySide6.QtGui import QDesktopServices
                from PySide6.QtCore import QUrl
                QDesktopServices.openUrl(QUrl(download_url))
        else:
            reply = QMessageBox()
            reply.setWindowTitle('检测更新')
            reply.setText('已是最新版本')
            reply.exec()
    except requests.RequestException:
        reply = QMessageBox()
        reply.setWindowTitle('检测更新')
        reply.setText('无法连接到更新服务器，请检查网络。')
        reply.exec()
