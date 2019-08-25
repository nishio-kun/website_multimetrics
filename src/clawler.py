"""
"""
import logging
from urllib.parse import urlsplit

import lxml.html
import readability

logging.getLogger('readability.readability').setLevel(logging.WARNING)


def get_content(html):
    """
    HTML の文字列から (タイトル, 本文) のタプルを取得します。
    """
    document = readability.Document(html)
    short_title = document.short_title()
    content_html = document.summary()
    content_text = lxml.html.fromstring(content_html).text_content().strip()

    return (short_title, content_text)


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


class Site:
    """
    WEB サイトクラス
    """
    def __init__(self, response):
        self.url = response.url
        self.response = response
        self.root = lxml.html.fromstring(response.content)
        self.root.make_links_absolute(response.url)
        self.related_site = self._list_related_site()

    def __repr__(self):
        return self.url

    def _list_related_site(self):
        """
        ページに記載されている他サイトの URL を取得します。
        """
        related_site = set()
        for a in self.root.cssselect('a'):
            url = a.get('href')
            if not url:
                continue
            related_site.add(parse_base_url(url))
        related_site.discard(self.url)
        return list(related_site)

    def list_article_url(self):
        """
        ルートのページの HtmlElement から記事ページの URL を抜き出します。
        """
        ret = set()
        for a in self.root.cssselect('a'):
            url = a.get('href')
            if parse_base_url(url) == self.url:
                ret.add(url)
        return sorted(list(ret))


class Page:
    """
    WEB ページクラス
    """
    def __init__(self, url, title, content):
        self.site = get_base_url(url)
        self.url = url
        self.title = title
        self.content = content

    def __repr__(self):
        return self.url


if __name__ == '__main__':
    import doctest
    doctest.testmod()
