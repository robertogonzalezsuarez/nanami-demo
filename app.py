import endpoints
import logging

from google.appengine.api.taskqueue import taskqueue
from google.appengine.ext import ndb
from protorpc import message_types
from protorpc import remote

from environment.environment import API_EXPLORER_CLIENT_ID
from helpers import gameHelper
from helpers import loginHelper
from helpers import matchmakingHelper
from messages.gameMessage import ShipsMessage, GameMessage, GameIdMessage
from messages.loginMessage import LoginMessage, LoginResponseMessage, IdMessage
from messages.shootMessage import ShootMessage
from models.profile import Profile

package = 'api'


def check_user(func):
    def check_user_decorator(service_instance, request):
        if request.id is None or request.id == '':
            raise endpoints.BadRequestException('Id de usuario no especificada')
        profile_key = ndb.Key(Profile, int(request.id))
        profile = profile_key.get()
        if not profile:
            raise endpoints.BadRequestException('Usuario no existe')
        return func(service_instance, request)

    return check_user_decorator


@endpoints.api(name='nanami', version='v1',
               allowed_client_ids=[API_EXPLORER_CLIENT_ID],
               scopes=[])
class NanamiApi(remote.Service):
    @endpoints.method(LoginMessage, LoginResponseMessage, path='login', http_method='POST',
                      name='login')
    def login(self, request):
        return loginHelper.login(request)

    @endpoints.method(IdMessage, message_types.VoidMessage, path='queue', http_method='POST', name='queue')
    @check_user
    def queue(self, request):
        return matchmakingHelper.queue(request)

    @endpoints.method(IdMessage, message_types.VoidMessage, path='unqueue', http_method='POST', name='unqueue')
    @check_user
    def unqueue(self, request):
        return matchmakingHelper.unqueue(request)

    @endpoints.method(IdMessage, message_types.VoidMessage, path='requeue', http_method='POST', name='requeue')
    @check_user
    def requeue(self, request):
        return matchmakingHelper.requeue(request)

    @endpoints.method(GameIdMessage, GameMessage, path='reMatch', http_method='POST', name='reMatch')
    def re_match(self, request):
        return gameHelper.re_match(request)

    @endpoints.method(IdMessage, message_types.VoidMessage, path='exitGame', http_method='POST', name='exitGame')
    @check_user
    def exit_game(self, request):
        return gameHelper.exit_game(request)

    @endpoints.method(ShipsMessage, message_types.VoidMessage, path='setShips', http_method='POST', name='setShips')
    def set_ships(self, request):
        return gameHelper.set_ships(request)

    @endpoints.method(ShootMessage, message_types.VoidMessage, path='shoot', http_method='POST', name='shoot')
    def shoot(self, request):
        taskqueue.add(url='/tasks/shoot',
                      params={'id': request.id, 'game': request.game, 'positions': str(request.positions)},
                      method="POST")
        return message_types.VoidMessage()


application = endpoints.api_server([NanamiApi], restricted=False)
