"""
Copyright: Digital Observatory 2023 <digitalobservatory@qut.edu.au>
Author: Mat Bettinson <mat.bettinson@qut.edu.au>
"""
import json
import re
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup


@dataclass
class VideoDetails:
    videoId: str
    title: str
    shortDescription: str
    lengthSeconds: int
    keywords: list[str] | None
    channelId: str
    author: str
    viewcount: int


def get_VideoDetails(url: str) -> VideoDetails | None:
    # Send a HTTP request to the given URL
    res = requests.get(url)
    # Throw an error if status is not 200
    res.raise_for_status()

    # Parse HTML response
    soup = BeautifulSoup(res.text, "html.parser")

    # Find body tag and then find next sibling script tag
    body = soup.body
    assert body is not None
    script = body.find("script")

    # If script tag is not found, return None
    if script is None:
        print("Script tag not found")
        return None

    # Extract JavaScript object using regex
    match = re.search(r"\{.*\}", script.text)

    # If object is not found, return None
    if match is None:
        print("JavaScript object not found")
        return None

    # Decode the JavaScript object into a Python dictionary
    obj = json.loads(match.group(0))
    vd = obj["videoDetails"]
    return VideoDetails(
        videoId=vd["videoId"],
        title=vd["title"],
        shortDescription=vd["shortDescription"],
        lengthSeconds=int(vd["lengthSeconds"]),
        keywords=vd["keywords"] if "keywords" in vd else None,
        channelId=vd["channelId"],
        author=vd["author"],
        viewcount=int(vd["viewCount"]),
    )
