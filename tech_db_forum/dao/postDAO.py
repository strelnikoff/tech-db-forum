import tech_db_forum.settings as settings
import postgresql
import falcon
import tech_db_forum.dao.forumDAO as forumDAO
import tech_db_forum.dao.userDAO as userDAO

from pytz import timezone


class PostDAO:

    def __init__(self):
        db_settings = settings.DatabaseSettings()
        self.db = postgresql.open(db_settings.get_command())

    def __del__(self):
        self.db.close()

    def get_details(self, post_id, related=[]):
        post = self.db.query("SELECT * FROM posts WHERE id={}".format(post_id))
        if len(post)==0:
            return {"message": "Post not found"}, falcon.HTTP_404
        post = {"post": self.post_from_table(post[0])}
        if related:
            related = related.split(",")
            for i in related:
                if i == "user":
                    user_dao = userDAO.UserDAO()
                    post["author"] = user_dao.get_user(post["post"]["author"])[0]
                if i == "forum":
                    forum_dao = forumDAO.ForumDAO()
                    post["forum"] = forum_dao.forum_info(post["post"]["forum"])
                if i == "thread":
                    import tech_db_forum.dao.threadDAO as threadDAO
                    thread_dao = threadDAO.ThreadDAO()
                    post["thread"] = thread_dao.get_details(post["post"]["thread"])[0]
        return post, falcon.HTTP_200

    def edit_post(self, post_id, post):
        post = self.check_post(post)
        upd_rows = None
        if len(post)!=0:
            upd_rows = self.db.query("UPDATE posts SET isedited=TRUE, message='{}' WHERE id={} AND message != '{}'".
                                     format( post["message"], post_id, post["message"]))
        if upd_rows is not None and str(upd_rows)[11] == '0':
            r = self.db.query("SELECT * FROM posts WHERE id={}".format(post_id))
            if len(r) > 0:
                return self.post_from_table(r[0]), falcon.HTTP_200
            return {"message": "Can't find post"}, falcon.HTTP_404
        r = self.post_from_table(self.db.query("SELECT * FROM posts WHERE id={}".format(post_id))[0])
        return r, falcon.HTTP_200

    def create_posts(self, slug_or_id, posts):
        pass

    def check_post(self, post):
        return post

    @staticmethod
    def post_from_table(t):
        return {
            "author": t["nickname"],
            "created": t["created"].astimezone(timezone('Europe/Moscow')).isoformat(),
            "forum": t["forum"],
            "id": t["id"],
            "isEdited": t["isedited"],
            "message": t["message"],
            "parent": t["parent"],
            "thread": t["thread"]
        }

