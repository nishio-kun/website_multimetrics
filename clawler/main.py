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
from src.es_util import upload


urls = [
    # 'https://gigazine.net/news/20190825-plastics-recycling/',
    'https://www.itmedia.co.jp/pcuser/articles/1908/25/news016.html',
    'https://gigazine.net/news/20190826-youtube-dmca-report-abuse/',
    'https://gigazine.net/news/20190826-teen-mental-health-tech-time/',
    'https://gigazine.net/news/20190825-fbi-quickly-build-trust/',
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

    time.sleep(30)
    for url in urls:
        temp_response = requests.get(url)
        upload(get_content(temp_response.content))
        time.sleep(1)


if __name__ == '__main__':
    main()
