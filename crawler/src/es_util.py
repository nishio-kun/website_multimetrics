import time

import elasticsearch


settings = {
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
    }
}

mappings = {
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


def connect():
    """
    elasticsearch のインデックスを作成します。
    """
    client = elasticsearch.Elasticsearch('localhost:9200')
    # client.indices.create(index='pages', body=settings)
    # client.indices.put_mapping(index='pages', body=mappings)
    client.indices.create(index='pages', body={'settings': settings['settings'], 'mappings': mappings['mappings']})
    return client


def upload(client, page):
    """
    WEB ページの辞書を elasticsearch にアップロードします。
    """
    client.index(index='pages', doc_type='_doc', body=page)


if __name__ == '__main__':
    main()
