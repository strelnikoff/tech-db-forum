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
        resp_body, resp_status = forum_dao.create_thread(name, doc)
        resp.body = json.dumps(resp_body)
        resp.status = resp_status


class Details(object):
    def on_get(self, resp, slug):
        forum_dao = forumDAO.ForumDAO()
        resp_body, resp_status = forum_dao.forum_info(slug)
        resp.body = json.dumps(resp_body)
        resp.status = resp_status


class Threads(object):
    def on_get(self, req, resp, name):
        forum_dao = forumDAO.ForumDAO()
        body = req.stream.read()
        resp_body, resp_status = forum_dao.get_forum_threads(name, body["limit"], body["since"], body["desc"])
        resp.body = json.dumps(resp_body)
        resp.status = resp_status


class Users(object):
    def on_get(self, req, resp, name):
        forum_dao = forumDAO.ForumDAO()
        body = req.stream.read()
        resp_body, resp_status = forum_dao.get_forum_users(name, body["limit"], body["since"], body["desc"])
        resp.body = json.dumps(resp_body)
        resp.status = resp_status
