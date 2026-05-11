import requests
from packaging import version
VERSION="v1.0.1"

def check_update(signal) -> None:
    api_url="https://api.github.com/repos/hhelibe2006-commits/LuxDown/releases/latest"
    try:
        response : requests.Response = requests.get(api_url)
        response.raise_for_status()
        data : dict = response.json()
        latest_version : str = data['tag_name']
        if version.parse(latest_version) > version.parse(VERSION):
            signal.emit(True, data['html_url'])
        else:
            signal.emit(False, None)

    except requests.RequestException:
        signal.emit('err', None)

