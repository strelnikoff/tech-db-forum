import json
import falcon


class Post(object):
    def on_post(self, req, resp, pid):
        doc = {
            'postTest': [
                pid
            ],
        }
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200

    def on_get(self, req, resp, pid):
        doc = {
            'postTest': [
                pid
            ],
        }
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200
