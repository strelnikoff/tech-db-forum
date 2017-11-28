import json
import falcon
import tech_db_forum.dao.forumDAO as forumDAO


class ForumCreate(object):
    def on_post(self, req, resp):
        if req.content_length in (None, 0):
            return

        body = req.stream.read()

        if not body:
            raise falcon.HTTP_BAD_REQUEST()

        try:
            doc = json.loads(body.decode('utf-8'))
        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTP_BAD_REQUEST()

        forum_dao = forumDAO.ForumDAO()
        resp_body, resp_status = forum_dao.forum_info(doc)
        resp.body = json.dumps(resp_body)
        resp.status = resp_status


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
    def on_get(self, resp, slug):
        forum_dao = forumDAO.ForumDAO()
        resp_body, resp_status = forum_dao.forum_info(slug)
        resp.body = json.dumps(resp_body)
        resp.status = resp_status


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
