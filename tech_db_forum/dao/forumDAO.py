import postgresql
import falcon
import tech_db_forum.settings as settings
import tech_db_forum.dao.userDAO as userDAO


class ForumDAO:
    def __init__(self):
        db_settings = settings.DatabaseSettings()
        self.db = postgresql.open(db_settings.get_command())

    def create_forum(self, forum):
        forum = self.check_forum(forum)
        user = self.db.query("SELECT * FROM users WHERE nickname = '{}'".format(forum["nickname"]))
        if len(user) != 0:
            return {
                       "message": "Can't find user"
                   }, falcon.HTTP_404
        forum_det = self.forum_info(forum["slug"])
        if len(forum_det.keys()) != 0:
            return forum_det, falcon.HTTP_409
        self.db.query("INSERT INTO forums(slug, title, nickname) VALUES ('{}', '{}', '{}')".format(
            forum["slug"], forum["title"], forum["nickname"]))
        return self.forum_info(forum["slug"]), falcon.HTTP_200

    # Не ясно что считать той же веткой
    def create_thread(self, slug, thread):
        thread = self.check_thread(thread)
        forum, code = self.get_forum_details(slug)
        if code == falcon.HTTP_404:
            return forum, code
        user_dao = userDAO.UserDAO()
        user, code = user_dao.get_user()
        if code == falcon.HTTP_404:
            return user, code
        thread_check = self.get_thread(slug, thread)
        if len(thread_check.keys()) > 0:
            return thread_check, falcon.HTTP_409
        if thread.get("slug") is None:
            self.db.query(
                "INSERT INTO threads (nickname, created, forum, message, title) VALUES ('{}','{}','{}','{}','{}')".format(
                    thread["nickname"], thread["created"], slug, thread["message"], thread["title"]
                ))
            return self.get_thread(slug, thread), falcon.HTTP_201
        else:
            self.db.query(
                "INSERT INTO threads (nickname, created, forum, message, title, slug) VALUES \
                ('{}','{}','{}','{}','{}','{}')".format(thread["nickname"], thread["created"], slug, thread["message"],
                                                        thread["title"], thread["slug"])
            )
            return self.get_thread(slug, thread), falcon.HTTP_201

    def get_forum_details(self, slug):
        forum_det = self.forum_info(slug)
        if len(forum_det.keys()) == 0:
            return {
                       "message": "Can't find forum"
                   }, falcon.HTTP_404
        return forum_det, falcon.HTTP_200

    # Тут нужно разобраться со временем
    def get_forum_threads(self, slug, limit, since, desc):
        forum, code = self.get_forum_details(slug)
        if code == falcon.HTTP_404:
            return forum, code
        query = "SELECT * FROM threads WHERE forum = '{}'".format(slug)
        if since is not None:
            query = query + " AND created >= '{}'".format(since)
        if limit is not None:
            query = query + " LIMIT {}".format(limit)
        if desc is not None:
            query = query + " ORDER BY created DESC"
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
        return self.thread_from_table(t)

    # По какому полю сортировать?
    def get_forum_users(self, slug, limit, since, desc):
        if limit is not None:
            limit = "LIMIT {}".format(limit)
        else:
            limit = ""
        if since is not None:
            since = " AND nickname != '{}'".format(since)
        else:
            since = ""
        if desc is not None:
            desc = " ORDER BY nickname"
        else:
            desc = ""
        t = self.db.query("SELECT * FROM users WHERE nickname IN (SELECT nickname FROM forums WHERE slug = \
                               '{}' {}){}{}".format(slug, since, desc, limit))
        result = []
        for i in t:
            result.append(userDAO.UserDAO.user_from_table(i))
        if len(result) == 0:
            return {"message": "Can't find forum"}, falcon.HTTP_404
        else:
            return result, falcon.HTTP_200

    def check_forum(self, forum):
        return forum

    def check_thread(self, thread):
        return thread

    # FIX IT
    def forum_info(self, slug):
        info = self.db.query("SELECT * FROM forums WHERE slug= '{}'".format(slug))
        if len(info) == 0:
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

    # FIX IT
    @staticmethod
    def thread_from_table(t):
        return {
            "author": t["nickname"],
            "created": t["created"],
            "forum": t["forum"],
            "id": t["id"],
            "message": t["message"],
            "slug": t["slug"],
            "title": t["title"],
            "votes": 0
            # "votes": t["votes"]
        }
