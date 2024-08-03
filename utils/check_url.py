import re

YOUTUBE_URL_REGEX = re.compile(
    r'^(https?://)?(www\.)?'
    r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
    r'(watch\?v=|embed/|v/|.+\?v=)[^&=%?]+'
)


def check_url(url: str):
    return YOUTUBE_URL_REGEX.match(url)


