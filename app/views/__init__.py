def get_paginated_list(model, results, schema, url, order, start, limit):
    # check if page exists
    count = len(results)
    if count < start:
        return {model: []}
    # make response
    obj = {'start': start, 'limit': limit, 'count': count}
    # make URLs
    # make previous url
    if start == 1:
        obj['previous'] = ''
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        obj['previous'] = url + '?start=%d' % start_copy
        if order:
            obj['previous'] = obj['previous'] + '&order=%s' % order
    # make next url
    if start + limit > count:
        obj['next'] = ''
    else:
        start_copy = start + limit
        obj['next'] = url + '?start=%d' % start_copy
        if order:
            obj['next'] = obj['next'] + '&order=%s' % order

    # finally extract result according to bounds
    results = results[(start - 1):(start - 1 + limit)]
    obj[model] = schema.dump(results, many=True)
    return obj
