import falcon
import json


class Profile(object):
    def on_get(self, req, resp, nickname):
        doc = {
            'user': [
                'profileGet',
                nickname
            ],
        }
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp, nickname):
        doc = {
            'user': [
                'profilePost',
                nickname
            ],
        }
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200


class Create(object):
    def on_post(self, req, resp, nickname):
        doc = {
            'user': [
                'createPost',
                nickname
            ],
        }
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200