import tech_db_forum.settings as settings
import postgresql
import falcon
import tech_db_forum.dao.forumDAO as forumDAO
import tech_db_forum.dao.userDAO as userDAO

from pytz import timezone


class PostDAO:
    db_settings = settings.DatabaseSettings()
    db = postgresql.open(db_settings.get_command())
    def __init__(self):
        pass

    def __del__(self):
        # self.db.close()
        pass

    def get_details(self, post_id, related=[]):
        data = "SELECT p.nickname as nickname, p.created as created, p.forum as forum, p.id as id, p.thread as thread," \
                "p.message as message, p.isedited as isedited, p.parent as parent "
        join = ""
        if related:
            related = related.split(",")
            for i in related:
                if i == "user":
                    data += ", u.fullname as fullname, u.email as email, u.about as about"
                    join += " INNER JOIN users as u ON u.nickname = p.nickname "
                if i == "forum":
                    data += ", f.title as ftitle, f.nickname as fnickname," \
                            "(SELECT COUNT(*) FROM posts WHERE forum =f.slug) AS posts," \
                            "(SELECT COUNT(*) FROM threads WHERE forum =f.slug) AS threads "
                    join += " INNER JOIN forums AS f ON p.forum=f.slug "
                if i == "thread":
                    data += ", t.message as tmessage, t.created as tcreated, t.votes as tvotes, t.slug as tslug," \
                             " t.nickname as tnickname, t.title as ttitle"
                    join += " INNER JOIN threads as t ON p.thread = t.id"
            join += " AND p.id={}".format(post_id)
        else:
            join = "WHERE p.id={}".format(post_id)

        query = "{} FROM posts as p {}".format(data, join)
        info = self.db.query(query)
        if len(info) == 0:
            return {"message": "Post not found"}, falcon.HTTP_404
        post = {"post": self.post_from_table(info[0])}
        if related:
            for i in related:
                if i == "user":
                    post["author"] = {"about": info[0]["about"], "email": info[0]["email"],
                                      "fullname": info[0]["fullname"],
                                      "nickname": info[0]["nickname"]}
                if i == "forum":
                    post["forum"] = {"slug": info[0]["forum"], "title": info[0]["ftitle"], "user": info[0]["fnickname"],
                                     "posts": info[0]["posts"], "threads": info[0]["threads"]
                                     }
                if i == "thread":
                    post["thread"] = {"author": info[0]["tnickname"], "created": info[0]["tcreated"].isoformat(),
                                      "forum": info[0]["forum"], "id": info[0]["thread"], "message": info[0]["tmessage"],
                                      "title": info[0]["ttitle"], "votes": info[0]["tvotes"]
                    }
                    if info[0]["tslug"]:
                        post["thread"]["slug"] = info[0]["tslug"]
        return post, falcon.HTTP_200

    def edit_post(self, post_id, post):
        if post.get("message"):
            post["values"] = "not exists(SELECT p.id FROM posts p WHERE p.message='{}' AND p.id = {}), '{}'".format(
                    post["message"], post_id, post["message"])
        else:
            post["values"] = "isedited, message"
        upd_rows = self.db.query("UPDATE posts SET (isedited, message) = ({}) WHERE id={} RETURNING *".
                                     format(post["values"], post_id, post.get("message")))
        if len(upd_rows) == 0:
            return {"message": "Can't find post"}, falcon.HTTP_404
        return self.post_from_table(upd_rows[0]), falcon.HTTP_200

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

