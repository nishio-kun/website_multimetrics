import time

import elasticsearch


mapping = {
    'mappings' : {
        '_doc' : {
            'properties' : {
                'title': {'type': 'text'},
                'content': {'type': 'text'}
            }
        }
    }
}


def upload(page):
    """
    WEB ページの辞書を elasticsearch にアップロードします。
    """
    client = elasticsearch.Elasticsearch('localhost:9200')
    client.indices.create(index='pages', body=mapping)

    client.index(index='pages', doc_type='_doc', body=page)


if __name__ == '__main__':
    main()
