"""module url.generate_url"""

import ssl
from urllib import error, request


def playlist_url(self, video_ids_url: str) -> str:
    """Generate the playlist URL from the video ids URL."""
    try:
        ctx = ssl._create_default_https_context()
        with request.urlopen(video_ids_url, context=ctx) as response:
            playlist_link = response.geturl()
            playlist_link = playlist_link.split("list=")[1]

        return (
            f"https://www.youtube.com/playlist?list={playlist_link}"
            + "&disable_polymer=true"
        )
    except (error.URLError, IndexError, UnicodeEncodeError):
        MainWindow.show_error_creating_url_dialog(self)
        logging.warning("An error occurred while generating the playlist URL!")
        return ""
