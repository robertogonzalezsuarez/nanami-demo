# -*- coding: utf-8 -*-
import endpoints
from protorpc import message_types

from firebaseService.firebaseService import Firebase
from helpers import firebaseHelper


def queue(request):
    if request.id is None or request.id == "":
        raise endpoints.BadRequestException('Por favor, inicia sesión para continuar.')
    auth_token = firebaseHelper.get_credentials()
    users = Firebase.get('/matchmaking/', auth_token)
    me = Firebase.get('/matchmaking/' + str(request.id), auth_token)
    if me is None:
        data = {'match': '0'}
        me = Firebase.patch('/matchmaking/' + request.id, data, auth_token)
    if users is not None:
        if me['match'] == '0':
            for user in users:
                if user != request.id and users[user]['match'] == '0':  # 0 means is not in any game, but queueing
                    data = {'player1': request.id, 'player2': user, 'player1_ready': False, 'player2_ready': False, 'status': 'SETTING'}
                    game = Firebase.post('/games/', data, auth_token)
                    patch_data = {'match': game['name']}
                    Firebase.patch('/matchmaking/' + request.id, patch_data, auth_token)
                    Firebase.patch('/matchmaking/' + str(user), patch_data, auth_token)
                    break
    return message_types.VoidMessage()


def unqueue(request):
    auth_token = firebaseHelper.get_credentials()
    me = Firebase.get('/matchmaking/' + str(request.id), auth_token)
    if me is not None:
        if me['match'] != '0':
            raise endpoints.BadRequestException(u'Ya estás en partida.')
        Firebase.delete('/matchmaking/' + str(request.id), auth_token)
    return message_types.VoidMessage()


def requeue(request):
    auth_token = firebaseHelper.get_credentials()
    me = Firebase.get('/matchmaking/' + str(request.id), auth_token)
    if me is not None and me['match'] != '0':
        game = Firebase.get('/games/' + str(me['match']), auth_token)
        if game is not None:
            if game['player1'] == str(request.id):
                if game['player2'] == '0':
                    Firebase.delete('/games/' + str(me['match']), auth_token)
                else:
                    Firebase.patch('/games/' + str(me['match']), {'player1': '0'}, auth_token)
            if game['player2'] == str(request.id):
                if game['player1'] == '0':
                    Firebase.delete('/games/' + str(me['match']), auth_token)
                else:
                    Firebase.patch('/games/' + str(me['match']), {'player2': '0'}, auth_token)
        Firebase.patch('/matchmaking/' + str(request.id), {'match': '0'}, auth_token)
    return queue(request)
