from os import abort


def get_paginated_list(results, schema, url, start, limit):
    # check if page exists
    count = len(results)
    if count < start:
        abort(404)
    # make response
    obj = {'start': start, 'limit': limit, 'count': count}
    # make URLs
    # make previous url
    if start == 1:
        obj['previous'] = ''
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        obj['previous'] = url + '?start=%d&limit=%d' % (start_copy, limit_copy)
    # make next url
    if start + limit > count:
        obj['next'] = ''
    else:
        start_copy = start + limit
        obj['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)
    # finally extract result according to bounds
    results = results[(start - 1):(start - 1 + limit)]
    obj['results'] = schema.dump(results, many=True)
    return obj
