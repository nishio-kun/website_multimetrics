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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url',
                        # required=True,
                        help='Website url')
    parser.add_argument('-o', '--out-file',
                        help='Output file')

    args = parser.parse_args()
    o_file = args.out_file or 'test.csv'

    # temp_response = requests.get(args.url)
    temp_response = requests.get('https://gigazine.net/news/20190825-plastics-recycling/')
    # temp_response = requests.get('https://www.itmedia.co.jp/pcuser/articles/1908/25/news016.html')
    time.sleep(1)
    response = requests.get(parse_base_url(temp_response.url))

    site = Site(response)
    # for url in site.list_article_url():
        # print(url)
    print(get_content(temp_response.content))


if __name__ == '__main__':
    main()
