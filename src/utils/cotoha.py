"""
COTOHA API を扱うモジュール。
"""
import json
import sys

import requests

sys.path.append('../')
import settings


ACCESS_TOKEN_PUBLISH_URL = settings.ACCESS_TOKEN_PUBLISH_URL
DEVELOPER_API_BASE_URL = settings.DEVELOPER_API_BASE_URL


def get_access_token(client_id, client_secret):
    """
    COTOHA API のトークンを取得します。
    """
    response = requests.post(ACCESS_TOKEN_PUBLISH_URL,
                             headers={'Content-Type': 'application/json'},
                             data=json.dumps({'grantType': 'client_credentials',
                                              'clientId': client_id,
                                              'clientSecret': client_secret}))

    return response.json().get('access_token')


def parse(token, sentense):
    """
    テキストを文節・形態素に分解します。
    """
    url = DEVELOPER_API_BASE_URL + 'nlp/v1/parse'
    token = 'Bearer ' + token
    data = json.dumps({'sentence': sentense, 'type': 'default'},
            ensure_ascii=False).encode('utf-8')
    response = requests.post(url=url,
                             headers={'Content-Type': 'application/json',
                                      'Authorization': token},
                             data=data)

    return response.json()


def extract_named_entity(token, sentense):
    """
    テキストに含まれる固有表現を抽出します。
    """
    url = DEVELOPER_API_BASE_URL + 'nlp/v1/ne'
    token = 'Bearer ' + token
    data = json.dumps({'sentence': sentense, 'type': 'default'},
            ensure_ascii=False).encode('utf-8')
    response = requests.post(url=url,
                             headers={'Content-Type': 'application/json',
                                      'Authorization': token},
                             data=data)

    return response.json()


def extract_keyword(token, sentense, upper):
    """
    テキストに含まれる特徴的なフレーズ・単語をキーワードとして抽出します。
    """
    url = DEVELOPER_API_BASE_URL + 'nlp/v1/keyword'
    token = 'Bearer ' + token
    data = json.dumps(
        {'document': sentense, 'type': 'default', 'max_keyword_num': upper},
        ensure_ascii=False
    ).encode('utf-8')
    response = requests.post(url=url,
                             headers={'Content-Type': 'application/json',
                                      'Authorization': token},
                             data=data)

    return response.json()


def attribute_user(token, sentense):
    """
    テキストから年代、性別、趣味、職業などの人物に関する属性を推定します。
    """
    url = DEVELOPER_API_BASE_URL + 'nlp/beta/user_attribute'
    token = 'Bearer ' + token
    data = json.dumps({'document': sentense, 'type': 'default'},
            ensure_ascii=False).encode('utf-8')
    response = requests.post(url=url,
                             headers={'Content-Type': 'application/json',
                                      'Authorization': token},
                             data=data)

    return response.json()


def get_morpheme(result):
    """
    構文解析結果から、原形と品詞名詞を抽出します。
    """
    ret = []
    for obj in result:
        for token in obj['tokens']:
            ret.append({'lemma': token['lemma'], 'pos': token['pos']})
    return ret


if __name__ == '__main__':
    def output(title, sentense, result):
        import pprint

        print('** ' + title + ' **')
        print(sentense)
        pprint.pprint(result)
        print()

    print('COTOHA API TEST\n')

    token = get_access_token(settings.DEVELOPER_CLIENT_ID,
                             settings.DEVELOPER_CLIENT_SECRET)
    sentense = '昨日母と銀座で焼き肉を食べた。'

    result = parse(token, sentense)
    output('構文解析', sentense, result)
    output('構文解析', sentense, get_morpheme(result['result']))

    output('固有表現抽出', sentense, extract_named_entity(token, sentense))
    output('キーワード抽出', sentense, extract_keyword(token, sentense, 10))
    output('ユーザ属性推定', sentense, attribute_user(token, sentense))
