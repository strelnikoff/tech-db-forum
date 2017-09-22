import json
import falcon


class Clear(object):
    def on_post(self, req, resp):
        doc = {
            'testService': [
                'clear'
            ],
        }
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200


class Status(object):
    def on_get(self, req, resp):
        doc = {
            'testService': [
                'status'
            ],
        }
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200
