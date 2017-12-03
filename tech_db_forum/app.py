import falcon
import tech_db_forum.forum as forum
import tech_db_forum.post as post
import tech_db_forum.service as service
import tech_db_forum.thread as thread
import tech_db_forum.user as user


api = application = falcon.API()

api.add_route('/forum/create', forum.ForumCreate())  # OK
api.add_route('/forum/{slug}/create', forum.ThreadCreate())  # OK
api.add_route('/forum/{slug}/details', forum.Details())  # OK
api.add_route('/forum/{slug}/threads', forum.Threads())  # OK
api.add_route('/forum/{slug}/details', forum.Users())  # OK

api.add_route('/post/{pid:int}/details', post.Post())  # OK

api.add_route('/service/clear', service.Clear())  # OK
api.add_route('/service/status', service.Status())  # OK

api.add_route('/thread/{tid}/create', thread.Create())
api.add_route('/thread/{tid}/details', thread.Details())  # OK
api.add_route('/thread/{tid}/posts', thread.Posts())
api.add_route('/thread/{tid}/vote', thread.Vote())

api.add_route('/user/{nickname}/create', user.Create())  # OK
api.add_route('/user/{nickname}/profile', user.Profile())  # OK
