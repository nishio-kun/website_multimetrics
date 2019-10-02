"""
Wayback Machine の Memento API を扱うモジュール。

cf.
https://ws-dl.blogspot.com/2013/07/2013-07-15-wayback-machine-upgrades.html
"""

import datetime
import re
import sys

import requests

sys.path.append('../')
import settings


WAYBACK_BASE_URL = settings.WAYBACK_BASE_URL


def convert_month_notation(month):
    """
    月の省略形を 0 埋め 2 桁の文字列に変換します。
    """
    month_pair = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                  'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
                  'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    return month_pair[month]


def get_first_date(raw):
    """
    Mement API の結果から、最初に収集された日時を取得します。
    """
    pattern = (r'"firstmemento";datetime="'
               r'(?P<youbi>[a-zA-Z]{3}),'
               r'(?P<day>\d{2})'
               r'(?P<month>[a-zA-Z]{3})'
               r'(?P<year>\d{4})'
               r'(?P<time>\d{2}:\d{2}:\d{2})'
               r'(?P<zone>[a-zA-Z]{3})"')

    content = ''
    for line in raw:
        content += line.rstrip()

    result = re.search(pattern, content)

    if result:
        ret = '/'.join([result.group('year'),
                        convert_month_notation(result.group('month')),
                        result.group('day')])
        return ret
    else:
        return ''


def list_timemap(url):
    """
    記事の収集された日時を取得します。
    """
    url = WAYBACK_BASE_URL + url
    response = requests.get(url)
    return response.text


if __name__ == '__main__':
    import argparse
    import pprint

    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', required=True, help='Website URL')
    args = parser.parse_args()

    print('Wayback Machine API TEST\n')

    response = list_timemap(args.url)
    pprint.pprint(get_first_date(response))
