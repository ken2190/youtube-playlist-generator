"""module playlist.video_info"""

import urllib

from bs4 import BeautifulSoup
from lxml import etree


def get_title_channel_from_youtube_link(video_id) -> str:
    """
    The get_title_channel_from_youtube_link function takes a YouTube video ID
    as an argument and returns the title of the video.

    :param video_id: Used to Specify the video id of the youtube link.
    :return: The title of the video from the youtube link.
    """
    with urllib.request.urlopen(f"https://www.youtube.com/watch?v={video_id}") as video:
        youtube = etree.HTML(video.read())
        video_title = youtube.xpath("//meta[@name='title']/@content")

    if video_title == [""]:
        return ""
    video_information = f"{video_title}"
    return "".join(video_information)


def get_video_length_from_video_id(video_id: str) -> str:
    """
    The get_video_length_from_video_id function takes a video_id
    as an argument and returns the length of the video.

    :param youtube_link: Used to Specify the youtube link.
    :return: The length of the video from the youtube link.
    """
    with urllib.request.urlopen(f"https://www.youtube.com/watch?v={video_id}") as video:
        html = etree.HTML(video.read())

        parsed_html = BeautifulSoup(html, features="lxml")

        print(parsed_html.title)  # Needs to be fixed

        return str(parsed_html.body.find("span", attrs={"class": "ytp-time-duration"}))


def get_video_thumbnail_url_from_video_id(video_id) -> str:
    """
    The get_video_thumbnail_url_from_video_id function accepts a video id
    and returns the url of the video's thumbnail.

    :param video_id: Used to Specify the video id.
    :return: The url of the video thumbnail.
    """
    with urllib.request.urlopen(
        f"img.youtube.com/vi/{video_id}/maxresdefault.jpg"
    ) as thumbnail:
        return etree.HTML(thumbnail.read())
