import json
import falcon
import tech_db_forum.dao.postDAO as postDAO


class Post(object):
    def on_post(self, req, resp, pid):
        if req.content_length in (None, 0):
            return

        body = req.stream.read()

        if not body:
            raise falcon.HTTP_BAD_REQUEST()

        try:
            doc = json.loads(body.decode('utf-8'))
        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTP_BAD_REQUEST()

        post_dao = postDAO.PostDAO()
        resp_body, resp_status = post_dao.edit_post(pid, doc)
        resp.body = json.dumps(resp_body)
        resp.status = resp_status

    def on_get(self, req, resp, pid):
        if req.content_length in (None, 0):
            return

        body = req.stream.read()

        if not body:
            raise falcon.HTTP_BAD_REQUEST()

        try:
            doc = json.loads(body.decode('utf-8'))
        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTP_BAD_REQUEST()

        post_dao = postDAO.PostDAO()
        resp_body, resp_status = post_dao.get_details(pid, doc)
        resp.body = json.dumps(resp_body)
        resp.status = resp_status
