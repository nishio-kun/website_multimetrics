"""
entry point
"""
import argparse
import logging
import sys
import time

import requests

from src.crawler import parse_base_url, Page
from src.es_util import upload, connect


# set logger
formatter = logging.Formatter('[%(levelname)-8s] %(message)s')
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

urls = [
    # 'https://www.itmedia.co.jp/pcuser/articles/1908/25/news016.html',

    'https://gigazine.net/news/20190825-plastics-recycling/',
    'https://gigazine.net/news/20190826-youtube-dmca-report-abuse/',
    'https://gigazine.net/news/20190826-teen-mental-health-tech-time/',
    'https://gigazine.net/news/20190825-fbi-quickly-build-trust/',
    'https://gigazine.net/news/20190827-matsuya-gourmet-set/',
    'https://gigazine.net/news/20190827-france-digital-tax-deal/',
    'https://gigazine.net/news/20190827-lucy-in-the-sky-trailer/',
    'https://gigazine.net/news/20190827-opioid-lawsuit-verdict/',
    'https://gigazine.net/news/20190826-google-bans-political-discussion/',
    'https://gigazine.net/news/20190826-trinitite-reminds-atomic-bomb-power/',
    'https://gigazine.net/news/20190826-industrial-revolution-hours-workweek/',
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url',
                        # required=True,
                        help='Website url')
    parser.add_argument('-n',
                        default=10,
                        type=int,
                        help='Number of pages you want to download')
    args = parser.parse_args()

    # queue = [args.url]
    queue = [urls[0]]
    done = []
    logger.info('Start crawling...')

    client = connect()

    n_downloaded = 0
    no_body = 0
    while args.n > n_downloaded - no_body:
        # download a page
        tmp_url = queue.pop(0)
        page = Page(tmp_url)
        page.download()
        page.get_content()

        n_downloaded += 1
        logger.info(f'{n_downloaded} page downloaded {page.url}')
        time.sleep(1)

        if not page.body:  # TODO:+ if 記事じゃない
            no_body += 1
            logger.info(f'not article or no body {page.url}')

        for url in page.list_article_url():
            if (not url in done) or (not url in queue) or (not url == tmp_url):
                queue.append(url)
        done.append(tmp_url)

        # insert data into elasticsearch
        upload(client,
               {'url': page.url, 'title': page.title, 'body': page.body})
        logger.debug('Inserted a page into elasticsearch')

        if len(queue) == 0:
            break

    logger.info(f'crawling finished successfully.')
    logger.info(f'{n_downloaded - no_body} pages saved.')
    logger.info(f'{no_body} pages have no body ({no_body / n_downloaded:.1%}).')


if __name__ == '__main__':
    main()
