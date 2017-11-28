import tech_db_forum.settings as settings
import postgresql
import falcon
import tech_db_forum.forum as forum
import tech_db_forum.user as user


class PostDAO:

    def __init__(self):
        db_settings = settings.DatabaseSettings()
        self.db = postgresql.open(db_settings.get_command())

    def get_details(self, post_id, related=[]):
        post = self.db.query("SELECT * FROM posts WHERE id={}".format(post_id))
        if len(post)==0:
            return {"message": "Post not found"}, falcon.HTTP_404
        post = {"post": self.post_from_table(post[0])}
        for i in related:
            if i=="author":
                user_dao = user.userDAO.UserDAO()
                post["author"] = user_dao.get_user(post["post"]["author"])
            if i=="forum":
                forum_dao = forum.forumDAO.ForumDAO()
                post["forum"] = forum_dao.forum_info(post["post"]["forum"])
            if i=="thread":
                pass
        return post, falcon.HTTP_200

    def edit_post(self, post_id, post):
        post = self.check_post(post)
        upd_rows=self.db.query("UPDATE posts SET nickname='{}', created='{}', forum='{}', isediter=TRUE, "
                               "message='{}', parent='{}',thread='{}' WHERE id={}".format(
            post["nickname"], post["created"], post["forum"], post["message"], post["parent"], post["thread"], post_id)
        )
        if upd_rows == 0:
            return {"message": "Can't find post"}, falcon.HTTP_404
        return post, falcon.HTTP_200


    def create_posts(self, slug_or_id, posts):
        pass

    def check_post(self, post):
        return post

    @staticmethod
    def post_from_table(self, t):
        return  {
            "author": t["nickname"],
            "created": t["created"],
            "forum": t["forum"],
            "id": t["id"],
            "isEdited": t["isEdited"],
            "message": t["message"],
            "parent": t["parent"],
            "thread": t["thread"]
        }

