"""
"""
import logging
from urllib.parse import urlsplit

import lxml.html
import readability
import requests


logging.getLogger('readability.readability').setLevel(logging.WARNING)


def parse_base_url(url):
    """
    基底 URL を取得します。

    >>> parse_base_url('https://www.itmedia.co.jp/keywords/nikon_z.html')
    'https://www.itmedia.co.jp/'

    >>> parse_base_url('https://gigazine.net/news/20190825-plastics-recycling/')
    'https://gigazine.net/'
    """

    parsed_url = urlsplit(url)
    base = f'{parsed_url[0]}://{parsed_url[1]}/'
    return base


class Page:
    """
    WEB ページクラス

    Attributes
    ----------
    url
    site_url
    response
    root
    title
    body
    """

    def __init__(self, url):
        self.url = url
        self.site_url = parse_base_url(url)

    def __repr__(self):
        return self.url

    def download(self):
        self.response = requests.get(self.url)
        self.root = lxml.html.fromstring(self.response.content)
        self.root.make_links_absolute(self.url)

    def get_content(self):
        """
        HTML の文字列から タイトル, 本文 を取得します。
        """
        document = readability.Document(self.response.content)
        title = document.title()
        content_html = document.summary()
        content_text = lxml.html.fromstring(content_html).text_content().strip()

        self.title = title
        self.body = content_text

    def list_article_url(self):
        """
        同じドメインの URL を抜き出します。
        """
        ret = set()
        for a in self.root.cssselect('a'):
            url = a.get('href')
            if parse_base_url(url) == self.site_url:
                ret.add(url)
        return list(ret)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
