import postgresql
import falcon
import tech_db_forum.settings as settings
import tech_db_forum.dao.userDAO as userDAO
import datetime
from dateutil.tz import tzlocal


class ForumDAO:
    def __init__(self):
        db_settings = settings.DatabaseSettings()
        self.db = postgresql.open(db_settings.get_command())

    def __del__(self):
        self.db.close()

    def create_forum(self, forum):
        try:
            result = self.db.query("INSERT INTO forums(slug, title, nickname) VALUES ('{}', '{}', "
                          "(SELECT nickname FROM users WHERE nickname = '{}')) RETURNING *".
                                   format(forum["slug"], forum["title"], forum["user"]))
            return self.forum_from_table(result[0]), falcon.HTTP_201
        except postgresql.exceptions.UniqueError:
            forum_det = self.get_forum(forum["slug"])
            return forum_det[0], falcon.HTTP_409
        except postgresql.exceptions.NotNullError:
            return {"message": "Can't find user"}, falcon.HTTP_404

    def create_thread(self, slug, thread):
        try:
            if thread.get("slug"):
                thread["slug"] = "'{}'".format(thread["slug"])
            else:
                thread["slug"] = "NULL"
            if not thread.get("created"):
                thread["created"] = datetime.datetime.now(tzlocal()).isoformat()
            result = self.db.query(
                "INSERT INTO threads (nickname, created, forum, message, title, slug) VALUES "
                "((SELECT nickname FROM users WHERE nickname = '{}'),'{}',(SELECT slug FROM forums WHERE slug = '{}'),"
                "'{}', '{}', {}) RETURNING *".format(thread["author"], thread["created"], slug, thread["message"],
                                                     thread["title"], thread["slug"])
            )
            return self.thread_from_table(result[0]), falcon.HTTP_201
        except postgresql.exceptions.UniqueError:
            thread = self.db.query("SELECT * FROM threads WHERE slug = {}".format(thread["slug"]))
            return self.thread_from_table(thread[0]), falcon.HTTP_409
        except postgresql.exceptions.NotNullError:
            return {"message": "Can't find"}, falcon.HTTP_404

    def get_forum(self, slug):
        info = self.db.query("SELECT * FROM forums WHERE slug = '{}'".format(slug))
        if len(info) == 0:
            return {}, falcon.HTTP_404
        return self.forum_from_table(info[0]), falcon.HTTP_200

    def get_forum_details(self, slug):
        forum_det = self.forum_info(slug)
        if len(forum_det.keys()) == 0:
            return {"message": "Can't find forum {}".format(slug)}, falcon.HTTP_404
        return forum_det, falcon.HTTP_200

    def get_forum_threads(self, slug, limit, since, desc):
        forum, code = self.get_forum(slug)
        if code == falcon.HTTP_404:
            return forum, code
        query = "SELECT * FROM threads WHERE forum = '{}'".format(slug)
        if since is not None:
            if desc == "true":
                query = query + " AND created <= '{}'".format(since)
            else:
                query = query + " AND created >= '{}'".format(since)
        query = query + " ORDER BY created"
        if desc == "true":
            query = query + " DESC"
        if limit is not None:
            query = query + " LIMIT {}".format(limit)
        info = self.db.query(query)
        result = []
        for i in info:
            result.append(self.thread_from_table(i))
        return result, falcon.HTTP_200

    # Тут нужно добавить голоса
    def get_thread(self, slug, thread):
        t = self.db.query("SELECT * FROM threads WHERE forum='{}' AND nickname='{}' AND \
                               message='{}' AND title='{}'".format(slug, thread["author"], thread["message"],
                                                                   thread["title"]))
        if len(t) == 0:
            return {}
        return self.thread_from_table(t[0])

    def get_forum_users(self, slug, limit, since, desc):
        forum, code = self.get_forum(slug)
        if code == falcon.HTTP_404:
            return {"message": "Can't find forum"}, falcon.HTTP_404
        if limit is not None:
            limit = "LIMIT {}".format(limit)
        else:
            limit = ""
        if since and desc == "true":
            since = " AND nickname < '{}' COLLATE ucs_basic".format(since)
        elif since:
            since = " AND nickname > '{}' COLLATE ucs_basic".format(since)
        else:
            since = ""
        if desc == "true":
            desc = " DESC"
        else:
            desc = ""

        t = self.db.query("SELECT * FROM (SELECT DISTINCT * FROM users WHERE (nickname IN (SELECT nickname FROM threads "
                          "WHERE forum='{}') OR nickname IN (SELECT nickname FROM posts WHERE "
                          "forum='{}')) {}) AS foo ORDER BY nickname COLLATE ucs_basic {} {};".
                          format(slug, slug, since, desc, limit));
        result = []
        for i in t:
            result.append(userDAO.UserDAO.user_from_table(i))
        return result, falcon.HTTP_200

    def check_forum(self, forum):
        return forum

    def check_thread(self, thread):
        return thread

    # FIX IT
    def forum_info(self, slug):
        info = self.db.query("SELECT * FROM forums WHERE slug = '{}'".format(slug))
        if len(info) == 0:
            return {}
        posts_count = self.db.query("SELECT COUNT(*) FROM posts WHERE forum = '{}'".format(slug))[0][0]
        threads_count = self.db.query("SELECT COUNT(*) FROM threads WHERE forum = '{}'".format(slug))[0][0]
        return {
            "posts": posts_count,
            "slug": info[0]["slug"],
            "threads": threads_count,
            "title": info[0]["title"],
            "user": info[0]["nickname"]
        }

    # FIX IT
    @staticmethod
    def forum_from_table(t):
        return {
            "posts": 0,
            "slug": t["slug"],
            "threads": 0,
            "title": t["title"],
            "user": t["nickname"]
        }

    @staticmethod
    def thread_from_table(t):
        result = {
            "author": t["nickname"],
            "created": t["created"].isoformat(),
            "forum": t["forum"],
            "id": t["id"],
            "message": t["message"],
            "title": t["title"],
            "votes": t["votes"]
        }
        if t["slug"]:
            result["slug"] = t["slug"]
        return result
