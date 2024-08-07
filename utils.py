import re

def get_url_in_string(text):
    url = re.search("(?P<url>https?://[^\\s]+)", text)
    if url is None:
        return None
    return url.group("url")