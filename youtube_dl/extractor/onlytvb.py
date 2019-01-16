# coding: utf-8
from __future__ import unicode_literals

import re

from .common import InfoExtractor


class OnlyTVBIE(InfoExtractor):
    # https://www.onetvb.com/section/play/153/14261
    _VALID_URL = r'https?://(?:www\.)?onetvb\.com/section/play/(?P<serie_id>[0-9]+)/(?P<id>[0-9]+)'
    _TEST = {
        'url': 'https://www.onetvb.com/section/play/153/14261',
        'md5': 'TODO: md5 sum of the first 10241 bytes of the video file (use --test)',
        'info_dict': {
            'id': '14261',
            'serie_id': '153',
            'ext': 'mp4',
            'title': 'Video title goes here',
            'thumbnail': r're:^https?://.*\.jpg$',
            # TODO more properties, either as:
            # * A value
            # * MD5 checksum; start the string with md5:
            # * A regular expression; start the string with re:
            # * Any Python type (for example int or float)
        }
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)
        base_url = "https://www.onetvb.com"
        # print(webpage)
        match = re.search('return "(.+)"',webpage)
        parser = match.group(1) # /parser?type=pmbestvbee&amp;url=3198736_FDNB4021416
        url = base_url + parser.replace("amp;", "")
        print(url)
        mp4html = self._download_webpage(url, video_id)

        if mp4html[0] == "{":
          # {"url":"OnlyTVB"}
          return
        match = re.search("url = '(.+)'\.",mp4html)
        src = match.group(1).replace("amp;", "")


        # TODO more code goes here, for example ...
        # title = self._html_search_regex(r'<h1>(.+?)</h1>', webpage, 'title')

        title = video_id
        desc = self._html_search_regex(r'<title>(.+?)</title>', webpage, 'title')
        print(desc)
        return {
            'id': video_id,
            'url': src,
            'title': title,
            'description': desc,
            # 'uploader': self._search_regex(r'<div[^>]+id="uploader"[^>]*>([^<]+)<', webpage, 'uploader', fatal=False),
            # TODO more properties (see youtube_dl/extractor/common.py)
        }
