from urllib.parse import urlparse

def is_url(url: str) -> bool:
    try:
        parsed_url = urlparse(url)
        return all([parsed_url.scheme, parsed_url.netloc])
    except ValueError:
        return False