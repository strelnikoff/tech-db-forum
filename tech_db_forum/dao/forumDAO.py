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

    def create_forum(self, forum):
        forum = self.check_forum(forum)
        user = self.db.query("SELECT * FROM users WHERE lower(nickname) = lower('{}')".format(forum["user"]))
        if len(user) != 1:
            return {"message": "Can't find user"}, falcon.HTTP_404
        user = userDAO.UserDAO.user_from_table(user[0])
        forum_det = self.forum_info(forum["slug"])
        if len(forum_det.keys()) != 0:
            return forum_det, falcon.HTTP_409
        self.db.query("INSERT INTO forums(slug, title, nickname) VALUES ('{}', '{}', '{}')".format(
            forum["slug"], forum["title"], user["nickname"]))
        forum["user"] = user["nickname"]

        return forum, falcon.HTTP_201

    # Не ясно что считать той же веткой
    def create_thread(self, slug, thread):
        thread = self.check_thread(thread)
        forum, code = self.get_forum_details(slug)
        if code == falcon.HTTP_404:
            return forum, code
        user_dao = userDAO.UserDAO()
        user, code = user_dao.get_user(thread.get("author"))
        if code == falcon.HTTP_404:
            return user, code
        if thread.get("slug"):
            thread_check = self.db.query("SELECT * FROM threads WHERE lower(slug) = lower('{}')".format(thread["slug"]))
            if len(thread_check) == 1:
                return self.thread_from_table(thread_check[0]), falcon.HTTP_409
        created_time = datetime.datetime.now(tzlocal()).isoformat()
        if thread.get("created") is None:
            thread["created"] = created_time
        if thread.get("slug") is None:
            self.db.query(
                "INSERT INTO threads (nickname, created, forum, message, title) VALUES ('{}','{}','{}','{}','{}')".format(
                    user["nickname"], thread["created"], forum["slug"], thread["message"], thread["title"]
                ))
            return self.get_thread(forum["slug"], thread), falcon.HTTP_201
        else:
            self.db.query(
                "INSERT INTO threads (nickname, created, forum, message, title, slug) VALUES \
                ('{}','{}','{}','{}','{}','{}')".format(user["nickname"], thread["created"], forum["slug"], thread["message"],
                                                        thread["title"], thread["slug"])
            )
            return self.get_thread(slug, thread), falcon.HTTP_201

    def get_forum_details(self, slug):
        forum_det = self.forum_info(slug)
        if len(forum_det.keys()) == 0:
            return {"message": "Can't find forum {}".format(slug)}, falcon.HTTP_404
        return forum_det, falcon.HTTP_200

    # Тут нужно разобраться со временем
    def get_forum_threads(self, slug, limit, since, desc):
        forum, code = self.get_forum_details(slug)
        if code == falcon.HTTP_404:
            return forum, code
        query = "SELECT * FROM threads WHERE lower(forum) = lower('{}')".format(slug)
        if since is not None:
            if desc == "true":
                query = query + " AND created <= '{}'".format(since)
            else:
                query = query + " AND created >= '{}'".format(since)
        query = query + " ORDER BY created"
        if desc == "true":
            query = query + " DESC"
        #if desc == "false":
        #    query = query + " ORDER BY created"
        if limit is not None:
            query = query + " LIMIT {}".format(limit)
        #print(query)
        info = self.db.query(query)
        result = []
        for i in info:
            result.append(self.thread_from_table(i))
        return result, falcon.HTTP_200

    # Тут нужно добавить голоса
    def get_thread(self, slug, thread):
        t = self.db.query("SELECT * FROM threads WHERE lower(forum)=lower('{}') AND nickname='{}' AND \
                               message='{}' AND title='{}'".format(slug, thread["author"], thread["message"],
                                                                   thread["title"]))
        if len(t) == 0:
            return {}
        return self.thread_from_table(t[0])

    # По какому полю сортировать?
    def get_forum_users(self, slug, limit, since, desc):
        forum, code = self.get_forum_details(slug)
        if code == falcon.HTTP_404:
            return {"message": "Can't find forum"}, falcon.HTTP_404
        if limit is not None:
            limit = "LIMIT {}".format(limit)
        else:
            limit = ""
        if since and desc == "true":
            since = " AND lower(nickname) < lower('{}') COLLATE ucs_basic".format(since)
        elif since:
            since = " AND lower(nickname) > lower('{}') COLLATE ucs_basic".format(since)
        else:
            since=""
        if desc == "true":
            desc = " DESC"
        else:
            desc = ""
        '''t = self.db.query("SELECT * FROM users WHERE nickname IN (SELECT DISTINCT posts.nickname AS nickname FROM posts \
                          INNER JOIN threads ON (posts.forum = threads.forum AND threads.forum = '{}' AND posts.forum = '{}')) \
                          {} ORDER BY lower(nickname) COLLATE ucs_basic {} {}".format(slug, slug, since, desc, limit))
        '''
        t = self.db.query("SELECT * FROM (SELECT DISTINCT * FROM users WHERE (nickname IN (SELECT nickname FROM threads "
                          "WHERE lower(forum)=lower('{}')) OR nickname IN (SELECT nickname FROM posts WHERE lower(forum)=lower('{}'))) {}) AS foo  "
                          "ORDER BY lower(nickname) COLLATE ucs_basic {} {};".format(slug, slug, since, desc, limit));
        result = []
        print("SELECT * FROM (SELECT DISTINCT * FROM users WHERE (nickname IN (SELECT nickname FROM threads "
                          "WHERE lower(forum)=lower('{}')) OR nickname IN (SELECT nickname FROM posts WHERE lower(forum)=lower('{}'))) {}) AS foo  "
                          "ORDER BY lower(nickname) COLLATE ucs_basic {} {};".format(slug, slug, since, desc, limit))
        for i in t:
            result.append(userDAO.UserDAO.user_from_table(i))
        if len(result) == 0:
            return [], falcon.HTTP_200
        else:
            return result, falcon.HTTP_200

    def check_forum(self, forum):
        return forum

    def check_thread(self, thread):
        return thread

    # FIX IT
    def forum_info(self, slug):
        info = self.db.query("SELECT * FROM forums WHERE lower(slug)= lower('{}')".format(slug))
        if len(info) == 0:
            return {}
        posts_count = self.db.query("SELECT COUNT(*) FROM posts WHERE lower(forum)= lower('{}')".format(slug))[0][0]
        threads_count = self.db.query("SELECT COUNT(*) FROM threads WHERE lower(forum)= lower('{}')".format(slug))[0][0]
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
        return {
            "author": t["nickname"],
            # datetime.datetime(2017, 2, 14, 11, 38, 18, 344000)
            # 2017-02-14T11:38:18.344+03:00
            "created": t["created"].isoformat(),
            "forum": t["forum"],
            "id": t["id"],
            "message": t["message"],
            "slug": t["slug"],
            "title": t["title"],
            "votes": t["votes"]
        }
