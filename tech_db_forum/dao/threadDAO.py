import postgresql
import falcon
import tech_db_forum.settings as settings
import tech_db_forum.dao.postDAO as postDAO
import datetime
from dateutil.tz import tzlocal


class ThreadDAO:
    db_settings = settings.DatabaseSettings()
    db = postgresql.open(db_settings.get_command())
    def __init__(self):
        pass

    def __del__(self):
        # self.db.close()
        pass

    # Ok
    def get_details(self, slug_or_id):
        try:
            thread_id = int(slug_or_id)
        except ValueError:
            thread_id = None
        if thread_id is not None:
            result = self.db.query("SELECT * FROM threads WHERE id={}".format(thread_id))
            if len(result) == 0:
                return {"message": "Can't find thread"}, falcon.HTTP_404
            return self.thread_from_table(result[0]), falcon.HTTP_200
        result = self.db.query("SELECT * FROM threads WHERE slug = '{}'".format(slug_or_id))
        if len(result) == 0:
            return {"message": "Can't find thread"}, falcon.HTTP_404
        return self.thread_from_table(result[0]), falcon.HTTP_200

    def get_posts(self, slug_or_id, limit, since, sort, desc):
        try:
            thread = "(SELECT id FROM threads WHERE id = {})".format(int(slug_or_id))
        except ValueError:
            thread = "(SELECT id FROM threads WHERE slug = '{}')".format(slug_or_id)
        thread = self.db.query(thread)
        if len(thread) == 0:
            return {"message": "Can't find"}, falcon.HTTP_404
        else:
            thread = thread[0]["id"]
        query = ""
        if limit is not None:
            limit = "LIMIT {}".format(limit)
        else:
            limit = ""
        if desc == "true":
            desc = " DESC"
        else:
            desc = ""
        if sort == "flat":
            if since is not None:
                if desc == " DESC":
                    since = " AND id < {}".format(since)
                else:
                    since = " AND id > {}".format(since)
            else:
                since = ""
            query = "SELECT * FROM posts WHERE thread={} {} ORDER BY created {}, id {} {}".format(thread, since, desc,
                                                                                                  desc, limit)
        elif sort == "tree":
            if since is not None:
                if desc == " DESC":
                    since = " AND path < (SELECT path FROM posts WHERE id={})".format(since)
                else:
                    since = " AND path > (SELECT path FROM posts WHERE id={})".format(since)
            else:
                since = ""
            query = "SELECT * FROM posts WHERE thread={} {} ORDER BY path {}, id {} {}".format(thread, since,
                                                                                               desc, desc, limit)
        elif sort == "parent_tree":
            query = "SELECT * FROM posts WHERE root IN (SELECT id FROM posts WHERE thread = {} AND parent = 0 ".\
                format(thread)
            if since is not None:
                if desc == " DESC":
                    query += " AND path < (SELECT path FROM posts WHERE id = {})".format(since)
                else:
                    query += " AND path > (SELECT path FROM posts WHERE id = {})".format(since)
            query += " ORDER BY id {} ".format(desc)
            if limit is not None:
                query += limit
            query += ") ORDER BY path {}".format(desc)
        else:
            if since is not None:
                if desc == " DESC":
                    since = " AND id < {}".format(since)
                else:
                    since = " AND id > {}".format(since)
            else:
                since = ""
            query = "SELECT * FROM posts WHERE thread = {} {} ORDER BY id {} {}".format(thread, since, desc, limit)

        posts = []
        result = self.db.query(query)
        for r in result:
            posts.append(postDAO.PostDAO.post_from_table(r))
        return posts, falcon.HTTP_200

    def create_posts(self, slug_or_id, posts):
        try:
            thread_inf = "(SELECT id, forum FROM threads WHERE id = {})".format(int(slug_or_id))
        except ValueError:
            thread_inf = "(SELECT id, forum FROM threads WHERE slug = '{}')".format(slug_or_id)
        thread_inf = self.db.query(thread_inf)
        if len(thread_inf) == 0:
            return {"message": "Can't find"}, falcon.HTTP_404
        else:
            thread = thread_inf[0]["id"]
            forum = thread_inf[0]["forum"]
        if len(posts) == 0:
            return [], falcon.HTTP_201
        created_time = datetime.datetime.now(tzlocal())
        result_posts = []
        values = ""
        for p in posts:
            if p.get("message") is None: p["message"] = ""
            if p.get("parent") is None: p["parent"] = 0
            values += "({}, '{}', '{}', '{}', '{}', {}), ".format(
                    thread, p["author"], forum, created_time, p["message"], p["parent"]
                )
        values = values[:-2]
        query = "INSERT INTO posts (thread, nickname, forum, created, message, parent) VALUES {} RETURNING *".format(values)

        try:
            r = self.db.query(query)
        except postgresql.exceptions.NotNullError:
            return {"message": "User error"}, falcon.HTTP_404
        if len(r) == 0:
            return {"message": "Parent thread error"}, falcon.HTTP_409
        for post in r:
            result_posts.append(postDAO.PostDAO.post_from_table(post))
        self.db.query("UPDATE forums SET posts = posts + {} WHERE slug = '{}';".format(len(result_posts), result_posts[0]["forum"]))
        #print(len(result_posts), result_posts[0]["forum"])
        return result_posts, falcon.HTTP_201

    def edit_thread(self, slug_or_id, thread):
        try:
            find = "id = {}".format(int(slug_or_id))
        except ValueError:
            find = "slug = '{}'".format(slug_or_id)
        if thread.get("message"):
            message = "'{}'".format(thread.get("message"))
        else:
            message = "message"
        if thread.get("title"):
            title = "'{}'".format(thread.get("title"))
        else:
            title = "title"
        query = "UPDATE threads SET (message, title) = ({}, {}) WHERE {} RETURNING *".format(message, title, find)
        result = self.db.query(query)
        if len(result) == 0:
            return {"message": "Can't find thread"}, falcon.HTTP_404
        return self.thread_from_table(result[0]), falcon.HTTP_200

    def vote_thread(self, slug_or_id, vote):
        try:
            thread = "(SELECT id FROM threads WHERE id = {})".format(int(slug_or_id))
        except ValueError:
            thread = "(SELECT id FROM threads WHERE slug = '{}')".format(slug_or_id)
        try:
            result = self.db.query("INSERT INTO votes (nickname, voice, thread) SELECT '{}', {}, {} RETURNING *".format(
                    vote["nickname"], vote["voice"], thread, vote["nickname"], thread)
            )
            if len(result) != 0:
                return self.thread_from_table(self.db.query("SELECT * FROM threads WHERE id={}".format(
                        result[0]["thread"]))[0]), falcon.HTTP_200
        except postgresql.exceptions.NotNullError:
            return {"message": "error"}, falcon.HTTP_404
        except postgresql.exceptions.ForeignKeyError:
            return {"message": "error"}, falcon.HTTP_404
        except postgresql.exceptions.UniqueError:
            pass
        try:
            result = self.db.query("UPDATE votes SET voice = {} WHERE id=(SELECT id FROM votes WHERE nickname = '{}' "
                          "AND thread = {} ) RETURNING *".format(int(vote["voice"]), vote["nickname"], thread))
            return self.thread_from_table(self.db.query("SELECT * FROM threads WHERE id={}".format(
                    result[0]["thread"]))[0]), falcon.HTTP_200
        except postgresql.exceptions.NotNullError:
            return {"message": "error"}, falcon.HTTP_404
        except postgresql.exceptions.ForeignKeyError:
            return {"message": "error"}, falcon.HTTP_404
        return {"message": "error"}, falcon.HTTP_404

    def get_thread_by_slug(self, slug):
        thread = self.db.query("SELECT * FROM threads WHERE slug = '{}' LIMIT 1".format(slug))
        if len(thread) == 0:
            return None
        return self.thread_from_table(thread[0])

    def check_thread_id(self, thread_id):
        thread = self.db.query("SELECT * FROM threads WHERE id = '{}' LIMIT 1".format(thread_id))
        if len(thread) == 0:
            return None
        return self.thread_from_table(thread[0])

    @staticmethod
    def vote_from_table(t):
        return {
            "nickname": t["nickname"],
            "voice": t["voice"],
            "thread": t["thread"],
            "id": t["id"]
        }

    @staticmethod
    def thread_from_table(t):
        return {
            "author": t["nickname"],
            "created": t["created"].isoformat(),
            "forum": t["forum"],
            "id": t["id"],
            "message": t["message"],
            "slug": t["slug"],
            "title": t["title"],
            "votes": t["votes"]
        }

    @staticmethod
    def check_vote(vote):
        return vote