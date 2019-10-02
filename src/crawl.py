"""
entry point
"""
import argparse
import logging
import sys

from elasticsearch import Elasticsearch

import settings
from utils.cotoha import get_access_token, get_morpheme, parse
from utils.crawler import get_page
from utils.es_util import download_all, indice, upload
from utils.wayback import get_first_date, list_timemap


# set logger
formatter = logging.Formatter('[%(levelname)-8s] %(message)s')
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', required=True, help='Website URL')
    parser.add_argument('-i', '--index', required=True, help='Index name')
    parser.add_argument('-n', default=10, type=int,
                        help='Number of pages you want to download')
    parser.add_argument('--no-cotoha', action='store_true',
                        help='Not use COTOHA API.')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    logger.info('Start crawling...')
    if args.no_cotoha:
        logger.info('no COTOHA API')

    queue = [args.url]
    done = []

    client = Elasticsearch(settings.HOST)
    index = f'pages-{args.index}'

    indice(client, index)
    done.extend(download_all(client, index, 'url'))

    token = get_access_token(settings.DEVELOPER_CLIENT_ID,
                             settings.DEVELOPER_CLIENT_SECRET)

    for i, page in enumerate(get_page(args.n, queue, done)):
        # Access COTOHA API.
        if not args.no_cotoha and page.body:
            morpheme = get_morpheme(parse(token, page.body)['result'])
        else:
            logger.debug('no body')
            morpheme = None

        # Access Wayback Machine.
        first_date = get_first_date(list_timemap(page.url))

        # Upload data into Elasticsearch
        upload(client, index, {'url': page.url,
                               'title': page.title,
                               'body': page.body,
                               'morpheme': morpheme,
                               'raw': page.response.text,
                               'first_date': first_date})
        logger.debug(f'{i + 1} Inserted: {page.url}')

        if len(queue) == 0:
            break

    logger.info(f'crawling finished successfully.')


if __name__ == '__main__':
    main()
