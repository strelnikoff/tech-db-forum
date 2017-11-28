import falcon
import json
from tech_db_forum.dao import userDAO


class Profile(object):

    def on_get(self, req, resp, nickname):
        user_dao = userDAO.UserDAO()
        resp_body, resp_status = user_dao.get_user(nickname)
        resp.body = json.dumps(resp_body)
        resp.status = resp_status

    def on_post(self, req, resp, nickname):
        if req.content_length in (None, 0):
            return

        body = req.stream.read()

        if not body:
            raise falcon.HTTP_BAD_REQUEST()

        try:
            doc = json.loads(body.decode('utf-8'))
        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTP_BAD_REQUEST()

        user_dao = userDAO.UserDAO()
        resp_body, resp_status = user_dao.edit_user(nickname, doc)
        resp.body = json.dumps(resp_body)
        resp.status = resp_status


class Create(object):

    def on_post(self, req, resp, nickname):
        if req.content_length in (None, 0):
            return

        body = req.stream.read()

        if not body:
            raise falcon.HTTP_BAD_REQUEST()

        try:
            doc = json.loads(body.decode('utf-8'))
        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTP_BAD_REQUEST()
        user_dao = userDAO.UserDAO()
        resp_body, resp_status = user_dao.create_user(nickname, doc)
        resp.body = json.dumps(resp_body)
        resp.status = resp_status