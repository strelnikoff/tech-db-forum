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
        resp_body, resp_status = forum_dao.create_forum(doc)
        resp.body = json.dumps(resp_body)
        resp.status = resp_status


class ThreadCreate(object):
    def on_post(self, req, resp, slug):
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
        resp_body, resp_status = forum_dao.create_thread(slug, doc)
        resp.body = json.dumps(resp_body)
        resp.status = resp_status


class Details(object):
    def on_get(self, req, resp, slug):
        forum_dao = forumDAO.ForumDAO()
        resp_body, resp_status = forum_dao.get_forum_details(slug)
        resp.body = json.dumps(resp_body)
        resp.status = resp_status


class Threads(object):
    def on_get(self, req, resp, slug):
        forum_dao = forumDAO.ForumDAO()
        resp_body, resp_status = forum_dao.get_forum_threads(slug, req.get_param("limit"), req.get_param("since"),
                                                             req.get_param("desc"))
        resp.body = json.dumps(resp_body)
        resp.status = resp_status

# Не верно
class Users(object):
    def on_get(self, req, resp, slug):
        forum_dao = forumDAO.ForumDAO()
        resp_body, resp_status = forum_dao.get_forum_users(slug, req.get_param("limit"), req.get_param("since"), req.get_param("desc"))
        resp.body = json.dumps(resp_body)
        resp.status = resp_status
