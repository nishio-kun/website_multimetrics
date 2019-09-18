"""
Elasticsearch, Kibana を扱うモジュール。
"""
import time

import elasticsearch


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


def download_all(client, index):
    """
    指定された index のデータを全て取得します。
    """
    ret = []
    data = client.search(index=index, scroll='2m',
                         body={'query': {'match_all': {}}})
    sid = data['_scroll_id']
    pages = data['hits']['hits']
    size = data['hits']['total']
    ret.extend(get_data(pages, 'url'))

    while size > 0:
        data = client.scroll(scroll_id=sid, scroll='2m')
        sid = data['_scroll_id']
        pages = data['hits']['hits']
        size = len(pages)
        ret.extend(get_data(pages, 'url'))

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
    client.index(index=index, doc_type='_doc', body=page)


if __name__ == '__main__':
    main()
