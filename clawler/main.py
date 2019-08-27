"""
entry point
"""
import argparse
import subprocess
import time

import requests

from src.clawler import (get_content,
                         parse_base_url,
                         Site)
from src.es_util import (upload,
                         connect)


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
    args = parser.parse_args()

#    temp_response = requests.get(args.url)
#    time.sleep(1)
#    response = requests.get(parse_base_url(temp_response.url))
#
#    site = Site(response)
#
#    for url in site.list_article_url():
#        print(url)

#    temp_response = requests.get(urls[0])
#    for key, value in get_content(temp_response.content).items():
#        print(key, value)
#
#    upload(get_content(temp_response.content))

    client = connect()
    counter = 0
    for url in urls:
        temp_response = requests.get(url)
        upload(client, get_content(temp_response.content))
        counter += 1
        print(f'{counter} page uploaded.')
        time.sleep(1)


if __name__ == '__main__':
    main()
