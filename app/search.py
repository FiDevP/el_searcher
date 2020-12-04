from app import app


def add_to_index(model):
    index = 'my_index'
    if not app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)

    app.elasticsearch.index(index=index, doc_type=index, id=model.id, body=payload)


def remove_from_index(model):
    index = 'my_index'
    if not app.elasticsearch:
        return
    app.elasticsearch.delete(index=index, doc_type=index, id=model.id)


def query_index(query):
    index = 'my_index'
    if not app.elasticsearch:
        return [], 0
    search = app.elasticsearch.search(
        index=index,
        doc_type=index,
        body={
            "size": 20,
            'query': {
                'match': {
                    'text': {
                        'query': query,
                        'operator': 'and'
                    }
                }
            }
        }
    )
    ids = [int(hit['_id']) for hit in search['hits']['hits']]

    return ids
