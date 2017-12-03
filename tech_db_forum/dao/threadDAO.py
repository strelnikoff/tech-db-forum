import postgresql
import falcon
import tech_db_forum.settings as settings


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
            return self.thread_from_table(result), falcon.HTTP_200
        result = self.db.query("SELECT * FROM threads WHERE slug={}".format(slug_or_id))
        if len(result) == 0:
            return {"message": "Can't find thread"}, falcon.HTTP_404
        return self.thread_from_table(result), falcon.HTTP_200

    def get_posts(self, slug_or_id, limit, since, sort, desc):
        if limit is not None:
            limit = "LIMIT {}".format(limit)
        else:
            limit = ""
        pass

    def create_posts(self, slug_or_id, posts):
        try:
            thread = self.check_thread_id(int(slug_or_id))
        except ValueError:
            thread = self.get_thread_by_slug(slug_or_id)
        if thread is None:
            return {"message": "Can't find thread"}, falcon.HTTP_404
        for p in posts:
            if self.get_parent_thread(p["parent"]) != thread:
                return {"message": "Parent thread error"}, falcon.HTTP_409


    def get_parent_thread(self, parent_id):
        result = self.db.query("SELECT thread FROM posts WHERE id = {}".format(parent_id))
        if len(result) == 0:
            return None
        return result["forum"]

    def edit_thread(self, slug_or_id, thread):
        try:
            thread_id = int(slug_or_id)
        except ValueError:
            thread_id = None
        if thread_id is not None:
            find = " id = {}".format(thread_id)
        else:
            find = " id = {}".format(slug_or_id)
        message = thread.get("message")
        title = thread.get("title")
        if message is not None: message = "message = {},".format(message)
        else: message = ""
        if title is not None: title = "title = {}".format(title)
        else: title = ""
        query = "UPDATE threads SET {} {} WHERE {}".format(message, title, find)
        result = self.db.query(query)
        if len(result)==0:
            return {"message": "Can't find thread"}, falcon.HTTP_404
        result = self.db.query("SELECT * FROM threads WHERE {}".format(find))
        return self.thread_from_table(result), falcon.HTTP_200

    def vote_thread(self, slug_or_id, vote):
        vote = self.check_vote(vote)
        try:
            thread = self.check_thread_id(int(slug_or_id))
        except ValueError:
            thread = self.get_thread_by_slug(slug_or_id)
        if thread is None:
            return {"message": "Can't find thread"}
        vote_last = self.get_vote(thread["id"], vote["nickname"])
        if vote_last is None:
            self.db.query("INSERT INTO votes (nickname, voice, thread) VALUES ('{}', {}, {})".format(
                vote["nickname"], vote["voice"], thread["id"]
            ))
            self.db.query("UPDATE threads SET (votes) VALUE (votes+({})) WHERE id = {}".format(vote, thread["id"]))
            thread["votes"] = thread["votes"] + vote["voice"]
            return thread, falcon.HTTP_200
        else:
            self.db.query("UPDATE votes SET (voice) VALUE ({})".format(int(vote["voice"])))
            self.db.query("UPDATE threads SET (votes) VALUE (votes+({})-({})) WHERE id = {}".format(
                vote["voice"], vote_last["voice"], thread["id"]))
            thread["votes"] = thread["votes"] - vote_last["voice"] + vote["voice"]
            return thread, falcon.HTTP_200

    def get_thread_by_slug(self, slug):
        thread = self.db.query("SELECT * FROM threads WHERE slug = '{}'".format(slug))
        if len(thread) == 0:
            return None
        return self.thread_from_table(thread)

    def check_thread_id(self, thread_id):
        thread = self.db.query("SELECT * FROM threads WHERE id = '{}'".format(thread_id))
        if len(thread) == 0:
            return None
        return self.thread_from_table(thread)

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
            "created": t["created"],
            "forum": t["forum"],
            "id": t["id"],
            "message": t["message"],
            "slug": t["slug"],
            "title": t["title"],
            "votes": 0
            # "votes": t["votes"]
        }

    @staticmethod
    def check_vote(vote):
        return vote