import requests
from packaging import version
VERSION = "v1.0.2"

def check_update(signal) -> None:
    api_url="https://api.github.com/repos/hhelibe2006-commits/LuxDown/releases/latest"
    try:
        response: requests.Response = requests.get(api_url)
        response.raise_for_status()
        data: dict = response.json()
        latest_version: str = data['tag_name']
        if version.parse(latest_version) > version.parse(VERSION):
            signal.emit('有新版本', '是否下载', True, data['html_url'])
        else:
            signal.emit('检测更新', '已是最新版本', False, '')
    except requests.RequestException:
        signal.emit('检测更新', '无法连接到更新服务器，请检查网络。', False, '')

