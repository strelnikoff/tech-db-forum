import json
import falcon


class ForumCreate(object):
    def on_post(self, req, resp):
        doc = {
            'testforum':[
                'OK'
            ],
        }
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200


class ThreadCreate(object):
    def on_post(self, req, resp, name):
        doc = {
            'testThread': [
                name
            ],
        }
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200


class Details(object):
    def on_get(self, req, resp, name):
        doc = {
            'testDetails': [
                name
            ],
        }
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200


class Threads(object):
    def on_get(self, req, resp, name):
        doc = {
            'testTreads': [
                name
            ],
        }
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200


class Users(object):
    def on_get(self, req, resp, name):
        doc = {
            'testUsers': [
                name
            ],
        }
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200
