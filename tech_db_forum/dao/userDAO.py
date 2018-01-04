import tech_db_forum.settings as settings
import postgresql
import falcon


class UserDAO:

    def __init__(self):
        db_settings = settings.DatabaseSettings()
        self.db = postgresql.open(db_settings.get_command())

    def __del__(self):
        self.db.close()

    #Возможно кусок с ошибкой медленный
    def create_user(self, nickname, profile):
        try:
            self.db.query("INSERT INTO users (nickname, about, email, fullname) VALUES ('{}', '{}', '{}', '{}')".format(
                    nickname, profile["about"], profile["email"], profile["fullname"]))
            profile["nickname"] = nickname
            return profile, falcon.HTTP_201
        except postgresql.exceptions.UniqueError:
            users = self.db.query("SELECT * FROM users WHERE nickname = '{}' OR email = '{}'".
                                  format(nickname, profile["email"]))
            result = []
            for t in users:
                result.append(self.user_from_table(t))
                # if result[len(result)-1]["nickname"] == nickname.lower():
                #     result[len(result) - 1]["nickname"] = nickname
            return result, falcon.HTTP_409

    def get_user(self, nickname):
        user = self.db.query("SELECT * FROM users WHERE nickname = '{}'".format(nickname))
        if len(user) == 1:
            result = self.user_from_table(user[0])
            return result, falcon.HTTP_200
        else:
            return {"message": "Can't find user with id"}, falcon.HTTP_404

    def edit_user(self, nickname, profile):
        try:
            set_query = ""
            if profile.get("about"):
                set_query += "'{}', ".format(profile.get("about"))
            else:
                set_query += "about, "
            if profile.get("email"):
                set_query += "'{}', ".format(profile.get("email"))
            else:
                set_query += "email, "
            if profile.get("fullname"):
                set_query += "'{}'".format(profile.get("fullname"))
            else:
                set_query += "fullname"
            user = self.db.query("UPDATE users SET (about, email, fullname) = ({}) WHERE nickname = '{}' RETURNING *".format(set_query, nickname))
            if(len(user) == 0):
                return {"message": "Can't find user with id"}, falcon.HTTP_404
            return self.user_from_table(user[0]), falcon.HTTP_200
        except postgresql.exceptions.UniqueError:
            return {"message": "User email is all ready use"}, falcon.HTTP_409

    @staticmethod
    def user_from_table(t):
        return {
            "about": t["about"],
            "email": t["email"],
            "fullname": t["fullname"],
            "nickname": t["nickname"]
        }