def get_paginated_list(model, results, schema, url, params, start, limit):
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
        obj['previous'] = url + f'?start={start_copy}' + params
    # make next url
    if start + limit > count:
        obj['next'] = ''
    else:
        start_copy = start + limit
        obj['next'] = url + f'?start={start_copy}' + params

    # finally extract result according to bounds
    results = results[(start - 1):(start - 1 + limit)]
    obj[model] = schema.dump(results, many=True)
    return obj
