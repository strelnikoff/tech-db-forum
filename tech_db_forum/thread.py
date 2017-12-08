import json
import falcon
import tech_db_forum.dao.threadDAO as threadDAO


class Create(object):
    def on_post(self, req, resp, tid):
        if req.content_length in (None, 0):
            return

        body = req.stream.read()

        if not body:
            raise falcon.HTTP_BAD_REQUEST()

        try:
            doc = json.loads(body.decode('utf-8'))
        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTP_BAD_REQUEST()

        thread_dao = threadDAO.ThreadDAO()
        resp_body, resp_status = thread_dao.create_posts(tid, doc)
        resp.body = json.dumps(resp_body)
        resp.status = resp_status


class Details(object):
    def on_get(self, req, resp, tid):
        thread_dao = threadDAO.ThreadDAO()
        resp_body, resp_status = thread_dao.get_details(tid)
        resp.body = json.dumps(resp_body)
        resp.status = resp_status

    def on_post(self, req, resp, tid):
        if req.content_length in (None, 0):
            return

        body = req.stream.read()

        if not body:
            raise falcon.HTTP_BAD_REQUEST()

        try:
            doc = json.loads(body.decode('utf-8'))
        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTP_BAD_REQUEST()

        thread_dao = threadDAO.ThreadDAO()
        resp_body, resp_status = thread_dao.edit_thread(tid, doc)
        resp.body = json.dumps(resp_body)
        resp.status = resp_status


class Posts(object):
    def on_get(self, req, resp, tid):
        thread_dao = threadDAO.ThreadDAO()
        resp_body, resp_status = thread_dao.get_posts(tid, req.get_param("limit"), req.get_param("since"),
                                                      req.get_param("sort"),  req.get_param("desc"))
        resp.body = json.dumps(resp_body)
        resp.status = resp_status


class Vote(object):
    def on_post(self, req, resp, tid):
        if req.content_length in (None, 0):
            return

        body = req.stream.read()

        if not body:
            raise falcon.HTTP_BAD_REQUEST()

        try:
            doc = json.loads(body.decode('utf-8'))
        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTP_BAD_REQUEST()

        thread_dao = threadDAO.ThreadDAO()
        resp_body, resp_status = thread_dao.vote_thread(tid, doc)
        resp.body = json.dumps(resp_body)
        resp.status = resp_status
