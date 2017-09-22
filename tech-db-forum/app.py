import falcon
import forum
import post
import service
import thread
import user


api = application = falcon.API()

api.add_route('/forum/create', forum.ForumCreate())
api.add_route('/forum/{name}/create', forum.ThreadCreate())
api.add_route('/forum/{name}/details', forum.Details())
api.add_route('/forum/{name}/threads', forum.Threads())
api.add_route('/forum/{name}/details', forum.Users())

api.add_route('/post/{pid:int}/details', post.Post())

api.add_route('/service/clear', service.Clear())
api.add_route('/service/status', service.Status())

api.add_route('/thread/{tid}/create', thread.Create())
api.add_route('/thread/{tid}/details', thread.Details())
api.add_route('/thread/{tid}/posts', thread.Posts())
api.add_route('/thread/{tid}/vote', thread.Vote())

api.add_route('/user/{nickname}/create', user.Create())
api.add_route('/user/{nickname}/profile', user.Profile())