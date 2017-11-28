
class ThreadDAO:
    def __init__(self, db):
        self.db = db

    def get_details(self, slug_or_id):
        pass

    def get_posts(self, slug_or_id, limit=0, since=0, sort="", desc=False):
        pass

    def slug_to_id(self, slug):
        pass

    def edit_thread(self, slug_or_id, thread):
        pass

    def vote_thread(self, slug_or_id):
        pass
