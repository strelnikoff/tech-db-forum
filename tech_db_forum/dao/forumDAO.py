
class ForumDAO:

    def __init__(self, db):
        self.db = db

    def create_forum(self, forum):
        pass

    def create_thread(self, slug, thread):
        pass

    def get_forum_details(self, slug):
        pass

    def get_forum_threads(self, slug, limit=0, since="", desc=False):
        pass

    def get_forum_users(self, slug, limit=0, since="", desc=False):
        pass
