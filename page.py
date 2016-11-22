def page_query(q, page=None, page_size=50):
    if page:
        query = q.limit(page_size)
        query = query.offset(page * page_size)
        return query
    return q
