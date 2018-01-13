import tech_db_forum.settings as settings
import postgresql
import falcon


class ServiceDAO:
    db_settings = settings.DatabaseSettings()
    db = postgresql.open(db_settings.get_command())
    def __init__(self):
        pass

    def __del__(self):
        # self.db.close()
        pass

    def clear(self):
        self.db.query("TRUNCATE TABLE users, posts, threads, votes, forums")
        return falcon.HTTP_200

    def status(self):
        result = {
            "forum": self.db.query("SELECT COUNT(*) FROM forums")[0][0],
            "post": self.db.query("SELECT COUNT(*) FROM posts")[0][0],
            "thread": self.db.query("SELECT COUNT(*) FROM threads")[0][0],
            "user": self.db.query("SELECT COUNT(*) FROM users")[0][0],
        }
        return result, falcon.HTTP_200
