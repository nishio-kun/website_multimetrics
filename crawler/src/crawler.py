"""
Web サイトから記事をダウンロード、パースするモジュール。
"""
import logging
import time
from urllib.parse import urlsplit

import lxml.html
import readability
import requests


# set logger
logging.getLogger('readability.readability').setLevel(logging.WARNING)


def get_page(n, queue, done):
    """
    記事をダウンロードします。
    """
    n_downloaded = 0
    no_body = 0
    while n > n_downloaded - no_body:
        tmp_url = queue.pop(0)
        page = Page(tmp_url)
        page.download()
        page.get_content()

        n_downloaded += 1
        # logger.debug(f'{n_downloaded} page downloaded {page.url}')
        time.sleep(1)

        if not page.body:  # TODO:+ if 記事じゃない
            no_body += 1
            # logger.info(f'not article or no body {page.url}')

        for url in page.list_article_url():
            if (not url in done) or (not url in queue) or (not url == tmp_url):
                queue.append(url)
            done.append(tmp_url)

        yield page


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
