import postgresql
import falcon
import tech_db_forum.settings as settings


class ForumDAO:

    def __init__(self):
        db_settings = settings.DatabaseSettings()
        self.db = postgresql.open(db_settings.get_command())

    def create_forum(self, forum):
        forum = self.check_forum(forum)
        user = self.db.query("SELECT * FROM users WHERE nickname = '{}'".format(forum["nickname"]))
        if len(user)!=0:
            return {
                "message":"Can't find user"
            }, falcon.HTTP_404
        forum_det = self.forum_info(forum["slug"])
        if len(forum_det.keys())!=0:
            return forum_det, falcon.HTTP_409
        self.db.query("INSERT INTO forums(slug, title, nickname) VALUES ('{}', '{}', '{}')".format(
            forum["slug"],forum["title"], forum["nickname"]))
        return self.forum_info(forum["slug"]), falcon.HTTP_200

    def create_thread(self, slug, thread):
        pass

    def get_forum_details(self, slug):
        forum_det = self.forum_info(slug)
        if len(forum_det.keys())==0:
            return {
                "message": "Can't find forum"
            }, falcon.HTTP_404
        return forum_det, falcon.HTTP_200

    def get_forum_threads(self, slug, limit=0, since="", desc=False):
        pass

    def get_forum_users(self, slug, limit=0, since="", desc=False):
        pass

    def check_forum(self, forum):
        return forum

    # FIX IT
    def forum_info(self, slug):
        info = self.db.query("SELECT * FROM forums WHERE slug= '{}'".format(slug))
        if len(info)==0:
            return {}
        return {
            "posts": 0,
            "slug": info[0]["slug"],
            "threads": 0,
            "title": info[0]["title"],
            "user": info[0]["nickname"]
        }

    @staticmethod
    def forum_from_table(t):
        return {
            "posts": 0,
            "slug": t["slug"],
            "threads": 0,
            "title": t["title"],
            "user": t["nickname"]
        }