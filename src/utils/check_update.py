VERSION="v1.0.0"
import requests
from packaging import version

def check_update(signal):
    api_url="https://api.github.com/repos/hhelibe2006-commits/LuxDown/releases/latest"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        latest_version = data['tag_name']
        if version.parse(latest_version) > version.parse(VERSION):
            signal.emit(True, data['html_url'])
        else:
            signal.emit(False, None)

    except requests.RequestException:
        signal.emit('err', None)

