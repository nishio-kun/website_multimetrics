"""
entry point
"""
import argparse
import logging
import sys

from elasticsearch import Elasticsearch
import requests

from src.crawler import get_page
from src.es_util import download_all, indice, upload


# set logger
formatter = logging.Formatter('[%(levelname)-8s] %(message)s')
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

HOST = 'localhost:9200'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url',
                        required=True,
                        help='Website url')
    parser.add_argument('-i', '--index',
                        required=True,
                        help='Index name')
    parser.add_argument('-n',
                        default=10,
                        type=int,
                        help='Number of pages you want to download')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    queue = [args.url]
    done = []
    logger.info('Start crawling...')

    client = Elasticsearch(HOST)
    index = f'pages-{args.index}'

    indice(client, index)
    done.extend(download_all(client, index))

    for i, page in enumerate(get_page(args.n, queue, done)):
        upload(client, index, {'url': page.url,
                               'title': page.title,
                               'body': page.body,
                               'raw': page.response.text})
        logger.debug(f'Inserted a page into elasticsearch {i} {page.url}')

        if len(queue) == 0:
            break

    logger.info(f'crawling finished successfully.')
    logger.info(f'{n_downloaded - no_body} pages saved.')


if __name__ == '__main__':
    main()
