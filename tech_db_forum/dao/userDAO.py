import tech_db_forum.settings as settings
import postgresql
import falcon


class UserDAO:

    def __init__(self):
        db_settings = settings.DatabaseSettings()
        self.db = postgresql.open(db_settings.get_command())

    def create_user(self, nickname, profile):
        profile = self.check_profile(profile)
        users = self.db.query("SELECT * FROM users WHERE nickname = '{}' OR email = '{}'".format(nickname,
                                                                                             profile["email"]))
        if len(users) != 0:
            result = []
            for t in users:
                result.append(self.user_from_table(t))
            return result, falcon.HTTP_409
        else:
            self.db.query("INSERT INTO users (nickname, about, email, fullname) VALUES ('{}', '{}', '{}', '{}')".format(
                nickname, profile["about"], profile["email"], profile["fullname"]))
            return profile, falcon.HTTP_201

    def get_user(self, nickname):
        user = self.db.query("SELECT * FROM users WHERE nickname = '{}'".format(nickname))
        if len(user) == 1:
            result = self.user_from_table(user[0])
            return result, falcon.HTTP_200
        else:
            return {"message": "Can't find user with id"}, falcon.HTTP_404

    def edit_user(self, nickname, profile):
        profile = self.check_profile(profile)
        user = self.db.query("SELECT * FROM users WHERE nickname = '{}'".format(nickname))
        if len(user) == 1:
            user = self.db.query("SELECT * FROM users WHERE email = '{}' and nickname != '{}'".format(profile["email"],
                                                                                                      nickname))
            if len(user)==0:
                self.db.query("UPDATE users SET about = '{}', email = '{}', fullname = '{}' WHERE nickname = '{}'".format(
                    profile["about"], profile["email"], profile["fullname"], nickname
                ))
                return profile, falcon.HTTP_200
            else:
                return {"message": "User email is all ready use"}, falcon.HTTP_409
        else:
            return {"message": "Can't find user with id"}, falcon.HTTP_404

    def check_profile(self, profile):
        return profile

    @staticmethod
    def user_from_table(t):
        return {
            "about":t["about"],
            "email":t["email"],
            "fullname":t["fullname"],
            "nickname":t["nickname"]
        }