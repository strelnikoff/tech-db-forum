import postgresql
import falcon
import tech_db_forum.settings as settings
import tech_db_forum.dao.userDAO as userDAO
import datetime
from dateutil.tz import tzlocal


class ForumDAO:
    db_settings = settings.DatabaseSettings()
    db = postgresql.open(db_settings.get_command())
    def __init__(self):
        pass

    def __del__(self):
        # self.db.close()
        pass

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
        #print(slug, limit, since, desc)
        query = "SELECT threads.slug, nickname,title, votes, created, message,id, forum, test.slug as test FROM threads "\
                "RIGHT JOIN (SELECT slug FROM forums WHERE slug='{}') AS test ON forum = '{}'".format(slug, slug)

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
        #print(query)
        result = []
        if len(info)==0 or info[0]["test"] is None:
            return {"message": "Can't find forum"}, falcon.HTTP_404
        if info[0]["id"] is None:
            return result, falcon.HTTP_200

        for i in info:
            result.append(self.thread_from_table(i))
        return result, falcon.HTTP_200

    def get_forum_users(self, slug, limit, since, desc):
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

        query ="SELECT nickname, email, about, fullname, test.slug "\
                          " FROM users RIGHT JOIN (SELECT slug FROM forums WHERE slug='{}') AS test "\
                          "ON nickname IN (SELECT nickname FROM forums_users "\
                          "WHERE slug = '{}') {} ORDER BY nickname COLLATE ucs_basic {} {}".format(slug, slug, since, desc, limit);
        t = self.db.query(query)
        if len(t)==0 or t[0]["slug"] is None:
            return {"message": "Can't find forum"}, falcon.HTTP_404
        result = []
        if t[0]["nickname"] is None:
            return result, falcon.HTTP_200
        for i in t:
            result.append(userDAO.UserDAO.user_from_table(i))
        return result, falcon.HTTP_200

    def forum_info(self, slug):
        info = self.db.query("SELECT * FROM forums WHERE slug ='{}';"
                             .format(slug, slug, slug))
        if len(info) == 0:
            return {}
        return {
            "posts": info[0]["posts"],
            "slug": info[0]["slug"],
            "threads": info[0]["threads"],
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
