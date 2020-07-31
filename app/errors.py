def page_not_found(e):
    return {'message': '존재하지 않는 글입니다.'}, 404


class IllegalStateError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
        self.message = message