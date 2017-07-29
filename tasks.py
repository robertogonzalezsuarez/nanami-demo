import webapp2

from tasksHelper.shootHelper import Shoot

APP = webapp2.WSGIApplication(
    [
        ('/tasks/shoot', Shoot)

    ], debug=True)