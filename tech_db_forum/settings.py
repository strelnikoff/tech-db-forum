
class DatabaseSettings:
    user = "forum"
    password = "forum"
    database = "tech_db"

    def get_command(self):
        return 'pq://{}:{}@localhost:5432/{}'.format(self.user, self.password, self.database)
