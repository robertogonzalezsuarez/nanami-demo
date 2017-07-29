import webapp2

from helpers import gameHelper


class Shoot(webapp2.RequestHandler):
    def post(self):
        gameHelper.shoot(self.request.get('game'), self.request.get('id'), eval(self.request.get('positions')))