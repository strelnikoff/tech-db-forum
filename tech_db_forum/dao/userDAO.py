import tech_db_forum.settings as settings
import postgresql
import falcon


class UserDAO:

    def __init__(self):
        db_settings = settings.DatabaseSettings()
        self.db = postgresql.open(db_settings.get_command())

    def __del__(self):
        self.db.close()

    def create_user(self, nickname, profile):
        profile = self.check_profile(profile)
        users = self.db.query("SELECT * FROM users WHERE lower(nickname) = lower('{}') OR lower(email) = lower('{}')".
                              format(nickname, profile["email"]))
        if len(users) != 0:
            result = []
            for t in users:
                result.append(self.user_from_table(t))
                if result[len(result)-1]["nickname"]==nickname.lower():
                    result[len(result) - 1]["nickname"] = nickname
            return result, falcon.HTTP_409
        else:
            self.db.query("INSERT INTO users (nickname, about, email, fullname) VALUES ('{}', '{}', '{}', '{}')".format(
                nickname, profile["about"], profile["email"], profile["fullname"]))
            profile["nickname"] = nickname
            return profile, falcon.HTTP_201

    def get_user(self, nickname):
        user = self.db.query("SELECT * FROM users WHERE lower(nickname) = lower('{}')".format(nickname))
        if len(user) == 1:
            result = self.user_from_table(user[0])
            return result, falcon.HTTP_200
        else:
            return {"message": "Can't find user with id"}, falcon.HTTP_404

    def edit_user(self, nickname, profile):
        profile = self.check_profile(profile)
        user = self.db.query("SELECT * FROM users WHERE lower(nickname) = lower('{}')".format(nickname))
        if len(user) == 1:
            user_conflict = None
            if profile.get("email"):
                user_conflict = self.db.query("SELECT * FROM users WHERE lower(email) = lower('{}') and "
                                              "nickname != lower('{}')".format(profile["email"], nickname))
            if user_conflict is None or len(user_conflict) == 0:
                set_query = ""
                if profile.get("about"):
                    set_query += "about = '{}' ".format(profile.get("about"))
                if profile.get("email"):
                    if set_query != "": set_query += ","
                    set_query += "email = '{}' ".format(profile.get("email"))
                if profile.get("fullname"):
                    if set_query != "": set_query += ","
                    set_query += "fullname = '{}'".format(profile.get("fullname"))
                if set_query != "":
                    self.db.query("UPDATE users SET {} WHERE lower(nickname) = lower('{}')".format(set_query, nickname))
                user = self.db.query("SELECT * FROM users WHERE lower(nickname) = lower('{}')".format(nickname))
                return self.user_from_table(user[0]), falcon.HTTP_200
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