import postgresql
import falcon
import tech_db_forum.settings as settings
import tech_db_forum.dao.postDAO as postDAO
import tech_db_forum.dao.userDAO as userDAO
import datetime
from dateutil.tz import tzlocal
from pytz import timezone


class ThreadDAO:
    def __init__(self):
        db_settings = settings.DatabaseSettings()
        self.db = postgresql.open(db_settings.get_command())

    def get_details(self, slug_or_id):
        try:
            thread_id = int(slug_or_id)
        except ValueError:
            thread_id = None
        if thread_id is not None:
            result = self.db.query("SELECT * FROM threads WHERE id={}".format(thread_id))
            if len(result)== 0:
                return {"message": "Can't find thread"}, falcon.HTTP_404
            return self.thread_from_table(result[0]), falcon.HTTP_200
        result = self.db.query("SELECT * FROM threads WHERE lower(slug)=lower('{}')".format(slug_or_id))
        if len(result) == 0:
            return {"message": "Can't find thread"}, falcon.HTTP_404
        return self.thread_from_table(result[0]), falcon.HTTP_200

    def get_posts(self, slug_or_id, limit, since, sort, desc):
        try:
            thread = self.check_thread_id(int(slug_or_id))
        except ValueError:
            thread = self.get_thread_by_slug(slug_or_id)
        if thread is None:
            return {"message": "Can't find thread"}, falcon.HTTP_404
        if limit is not None:
            limit = "LIMIT {}".format(limit)
        else:
            limit = ""
        if desc is not None:
            desc = " DESC"
        else:
            desc = ""
        if since is not None:
            print(since)
            if desc == " DESC":
                since = " AND path < {}".format(since)
            else:
                since = " AND id > {}".format(since)
        else:
            since = ""
        if sort == "flat":
            result = self.db.query("SELECT * FROM posts WHERE thread={} {} ORDER BY created, id {} {}".format(thread["id"], since, desc, limit))
            posts=[]
            for r in result:
                posts.append(postDAO.PostDAO.post_from_table(r))
            return posts, falcon.HTTP_200
        if sort == "tree":
            result = self.db.query(
                "SELECT * FROM posts WHERE thread={} {} ORDER BY path {} {}".format(thread["id"], since, desc,
                                                                                          limit))
            posts = []
            for r in result:
                posts.append(postDAO.PostDAO.post_from_table(r))
            return posts, falcon.HTTP_200
        pass

    def create_posts(self, slug_or_id, posts):
        try:
            thread = self.check_thread_id(int(slug_or_id))
        except ValueError:
            thread = self.get_thread_by_slug(slug_or_id)
        if thread is None:
            return {"message": "Can't find thread"}, falcon.HTTP_404
        if len(posts) == 0:
            return [], falcon.HTTP_201
        user_dao = userDAO.UserDAO()
        user, code = user_dao.get_user(posts[0]["author"])
        if code == falcon.HTTP_404:
            return {"message": "Can't find user"}, falcon.HTTP_404
        for p in posts:
            if p.get("parent"):
                if self.get_parent_thread(p.get("parent")) != thread["id"]:
                    print(thread, p.get("parent"))
                    return {"message": "Parent thread error"}, falcon.HTTP_409
        created_time = datetime.datetime.now(tzlocal())#.isoformat()
        result_posts = []
        ins = self.db.prepare("INSERT INTO posts (thread, nickname, forum, created, message, parent) VALUES "
                              "($1, $2, $3, $4, $5, $6) RETURNING *")
        for p in posts:
            if p.get("message") is None: p["message"] = ""
            if p.get("parent") is None: p["parent"] = 0
            result_posts.append(postDAO.PostDAO.post_from_table(ins(thread["id"], user["nickname"], thread["forum"],created_time, p["message"], p["parent"])[0]))
        return result_posts, falcon.HTTP_201

    def get_parent_thread(self, parent_id):
        result = self.db.query("SELECT thread FROM posts WHERE id = {}".format(parent_id))
        if len(result) == 0:
            return None
        return result[0]["thread"]

    def edit_thread(self, slug_or_id, thread):
        try:
            thread_id = int(slug_or_id)
        except ValueError:
            thread_id = None
        if thread_id is not None:
            find = " id = {}".format(thread_id)
        else:
            find = " lower(slug) = lower('{}')".format(slug_or_id)
        if len(thread) == 0:
            result = self.db.query("SELECT * FROM threads WHERE {}".format(find))
            return self.thread_from_table(result[0]), falcon.HTTP_200
        message = thread.get("message")
        title = thread.get("title")
        if message is not None: message = "message = '{}'".format(message)
        else: message = ""
        if title is not None:
            if message != "":
                message += ","
            title = "title = '{}'".format(title)
        else: title = ""
        query = "UPDATE threads SET {} {} WHERE {}".format(message, title, find)
        #print(query)
        result = self.db.query(query)
        result=str(result)
        print(len(result))
        if result[11] == '0':
            return {"message": "Can't find thread"}, falcon.HTTP_404
        result = self.db.query("SELECT * FROM threads WHERE {}".format(find))
        return self.thread_from_table(result[0]), falcon.HTTP_200

    def vote_thread(self, slug_or_id, vote):
        vote = self.check_vote(vote)
        try:
            thread = self.check_thread_id(int(slug_or_id))
        except ValueError:
            thread = self.get_thread_by_slug(slug_or_id)
        if thread is None:
            return {"message": "Can't find thread"}, falcon.HTTP_404
        user_dao = userDAO.UserDAO()
        user, code = user_dao.get_user(vote["nickname"])
        if code == falcon.HTTP_404:
            return {"message": "Can't find user"}, falcon.HTTP_404
        vote_last = self.get_vote(thread["id"], vote["nickname"])
        if vote_last is None:
            self.db.query("INSERT INTO votes (nickname, voice, thread) VALUES ('{}', {}, {})".format(
                vote["nickname"], vote["voice"], thread["id"]
            ))
            self.db.query("UPDATE threads SET votes = votes+({}) WHERE id = {}".format(vote["voice"], thread["id"]))
            thread["votes"] = thread["votes"] + vote["voice"]
            return thread, falcon.HTTP_200
        else:
            self.db.query("UPDATE votes SET voice = {}".format(int(vote["voice"])))
            self.db.query("UPDATE threads SET votes = votes+({})-({}) WHERE id = {}".format(
                vote["voice"], vote_last[0]["voice"], thread["id"]))
            thread["votes"] = thread["votes"] - vote_last[0]["voice"] + vote["voice"]
            return thread, falcon.HTTP_200

    def get_thread_by_slug(self, slug):
        thread = self.db.query("SELECT * FROM threads WHERE lower(slug) = lower('{}')".format(slug))
        if len(thread) == 0:
            return None
        return self.thread_from_table(thread[0])

    def check_thread_id(self, thread_id):
        thread = self.db.query("SELECT * FROM threads WHERE id = '{}'".format(thread_id))
        if len(thread) == 0:
            return None
        return self.thread_from_table(thread[0])

    def get_vote(self, thread_id, nickname):
        vote = self.db.query("SELECT * FROM votes WHERE thread = {} AND nickname = '{}'".format(thread_id, nickname))
        if len(vote) == 0:
            return None
        return vote

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