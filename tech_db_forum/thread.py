import json
import falcon


class Create(object):
    def on_post(self, req, resp, tid):
        doc = {
            'thread': [
                'create',
                tid
            ],
        }
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200


class Status(object):
    def on_get(self, req, resp, tid):
        doc = {
            'thread': [
                'status',
                tid
            ],
        }
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200


class Details(object):
    def on_get(self, req, resp, tid):
        doc = {
            'thread': [
                'detailsGet',
                tid
            ],
        }
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp, tid):
        doc = {
            'thread': [
                'detailsPost',
                tid
            ],
        }
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200


class Posts(object):
    def on_get(self, req, resp, tid):
        doc = {
            'thread': [
                'postsGet',
                tid
            ],
        }
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200


class Vote(object):
    def on_get(self, req, resp, tid):
        doc = {
            'thread': [
                'vote',
                tid
            ],
        }
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200