"""
Elasticsearch, Kibana を扱うモジュール。
"""
import logging
import sys
import time

import elasticsearch


formatter = logging.Formatter('[%(levelname)-8s] %(message)s')
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


BODY = {
    'settings': {
        'analysis': {
            'tokenizer': {
                'kuromoji_tokenizer': {
                    'type': 'kuromoji_tokenizer',
                    'mode' : 'search',
                }
            },
            'analyzer': {
                'kuromoji_analyzer': {
                    'type': 'custom',
                    'tokenizer': 'kuromoji_tokenizer'
                }
            }
        }
    },
    'mappings' : {
        '_doc' : {
            'properties' : {
                'title': {
                    'type': 'text',
                    'analyzer': 'kuromoji_analyzer',
                    'fielddata': True,
                    'fields': {
                        'keyword': {
                            'type': 'keyword',
                            'ignore_above': 256
                        }
                    }
                },
                'body': {
                    'type': 'text',
                    'analyzer': 'kuromoji_analyzer',
                    'fielddata': True,
                    'fields': {
                        'keyword': {
                            'type': 'keyword',
                            'ignore_above': 256
                        }
                    }
                }
            }
        }
    }
}


def download_all(client, index, field):
    """
    指定された index のデータを全て取得します。
    """
    ret = []
    data = client.search(index=index, scroll='2m',
                         body={'query': {'match_all': {}}})
    sid = data['_scroll_id']
    pages = data['hits']['hits']
    size = data['hits']['total']
    ret.extend(get_data(pages, field))

    while size > 0:
        data = client.scroll(scroll_id=sid, scroll='2m')
        sid = data['_scroll_id']
        pages = data['hits']['hits']
        size = len(pages)
        ret.extend(get_data(pages, field))

    return ret


def indice(client, index):
    """
    指定された index を作成します。
    """
    try:
        client.indices.create(index=index, body=BODY)
    except elasticsearch.exceptions.RequestError as e:
        if e.info['error']['root_cause'][0]['type'] == \
                'resource_already_exists_exception':
            pass
        else:
            raise
    except Exception:
        raise


def get_data(pages, field):
    """
    指定された field のデータを取得します。
    """
    ret = []
    for page in pages:
        ret.append(page['_source'][field])
    return ret


def upload(client, index, page):
    """
    WEB ページの辞書を elasticsearch にアップロードします。
    """
    try:
        client.index(index=index, doc_type='_doc', body=page)
    except elasticsearch.exceptions.RequestError as e:
        if e.info['error']['root_cause'][0]['type'] == \
                'mapper_parsing_exception':
            logger.error(f'"mapper_parsing_exception" has occerred. '
                         f'"date" field was "{page["first_date"]}"')
        else:
            raise
    except Exception:
        raise


if __name__ == '__main__':
    main()
