import json
from tech_db_forum.dao import serviceDAO


class Clear(object):
    def on_post(self, req, resp):
        service_dao = serviceDAO.ServiceDAO()
        resp.status = service_dao.clear()


class Status(object):
    def on_get(self, req, resp):
        service_dao = serviceDAO.ServiceDAO()
        resp_body, resp_status = service_dao.status()
        resp.body = json.dumps(resp_body, ensure_ascii=False)
        resp.status = resp_status
