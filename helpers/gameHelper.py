# -*- coding: utf-8 -*-
import endpoints
import logging
from protorpc import message_types
from datetime import datetime
import time

from firebaseService.firebaseService import Firebase
from helpers import firebaseHelper
from messages.gameMessage import GameMessage


def exit_game(request):
    auth_token = firebaseHelper.get_credentials()
    me = Firebase.get('/matchmaking/' + str(request.id), auth_token)
    if me is not None and me['match'] != '0':
        game = Firebase.get('/games/' + str(me['match']), auth_token)
        if game is not None:
            if game['player1'] == str(request.id):
                if game['player2'] == '0':
                    Firebase.delete('/games/' + str(me['match']), auth_token)
                else:
                    Firebase.patch('/games/' + str(me['match']), {'player1': '0','status': 'ENDED'}, auth_token)
            if game['player2'] == str(request.id):
                if game['player1'] == '0':
                    Firebase.delete('/games/' + str(me['match']), auth_token)
                else:
                    Firebase.patch('/games/' + str(me['match']), {'player2': '0','status': 'ENDED'}, auth_token)


    Firebase.delete('/matchmaking/' + str(request.id), auth_token)
    return message_types.VoidMessage()


def set_ships(request):
    auth_token = firebaseHelper.get_credentials()
    game = Firebase.get('/games/' + str(request.game), auth_token)
    if not game:
        raise endpoints.BadRequestException(u'La partida no existe.')
    player = ''
    enemy_player = ''
    if game['player1'] == request.id:
        player = 'player1'
        enemy_player = 'player2'
    if game['player2'] == request.id:
        player = 'player2'
        enemy_player = 'player1'
    if player == '':
        raise endpoints.BadRequestException(u'El jugador no está en esta partida.')
    ships_positions = []
    ships_hit = []
    for ship in request.ships:
        ships_positions.append({ship.name: ship.positions})
        initialize_hit = []
        for position in ship.positions:
            initialize_hit.append(False)
        ships_hit.append({ship.name: initialize_hit})
    new_data = {player + '_ready': True}
    data_ships = {player + '_ships': ships_positions, player + '_hit': ships_hit}
    if game[enemy_player + '_ready']:
        new_data['status'] = 'ONGOING'
    Firebase.patch('/games/' + str(request.game), new_data, auth_token)
    Firebase.patch('/games/' + str(request.game) + '/ships/', data_ships, auth_token)
    return message_types.VoidMessage()


def re_match(request):
    auth_token = firebaseHelper.get_credentials()
    game = Firebase.get('/games/' + str(request.game), auth_token)
    if not game:
        raise endpoints.BadRequestException('La partida no existe')
    if game['status'] != 'ENDED':
        raise endpoints.BadRequestException('La partida no ha acabado.')
    player1 = game['player1']
    player2 = game['player2']
    if player1 != request.id and player2 != request.id:
        raise endpoints.BadRequestException('El jugador no se encuentra en esta partida')
    if player1 == '0' or player2 == '0':
        raise endpoints.BadRequestException('Uno de los dos jugadores ya ha abandonado la partida.')
    if 'rematch_request' not in game:
        Firebase.patch('/games/' + str(request.game), {'rematch_request': request.id}, auth_token)
        return GameMessage(game=request.game)
    if game['rematch_request'] == request.id:
        return GameMessage(game=request.game)
    Firebase.delete('/games/' + str(request.game), auth_token)
    data = {'player1': player1, 'player2': player2, 'player1_ready': False, 'player2_ready': False, 'status': 'SETTING'}
    new_game = Firebase.post('/games/', data, auth_token)
    Firebase.patch('/matchmaking/' + str(player1), {'match': new_game}, auth_token)
    Firebase.patch('/matchmaking/' + str(player2), {'match': new_game}, auth_token)
    return GameMessage(game=str(new_game))


def shoot(game_id, id, positions):
    auth_token = firebaseHelper.get_credentials()
    game = Firebase.get('/games/' + str(game_id), auth_token)
    if not game:
        # raise endpoints.BadRequestException('La partida no existe.')
        return message_types.VoidMessage()
    enemy_player = ''
    if game['player1'] == str(id):
        enemy_player = 'player2'
    if game['player2'] == str(id):
        enemy_player = 'player1'
    if enemy_player == '':
        return message_types.VoidMessage()
        # raise endpoints.BadRequestException('No estás en esta partida.')
    if game['status'] != "ONGOING":
        return message_types.VoidMessage()
        # raise endpoints.BadRequestException('La partida no está en ejecución')
    enemy_ships = game['ships'][enemy_player + '_ships']
    enemy_hit = game['ships'][enemy_player + '_hit']
    hit, new_hit, position_hit = calculate_hits(positions, enemy_ships, enemy_hit)
    new_shoot = {'player': id, 'positions': positions, 'hit': position_hit }
    Firebase.patch('/games/' + str(game_id) + '/shoots/',
                   {str(int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds() * 1000)): new_shoot},
                   auth_token)
    Firebase.patch('/games/' + str(game_id) + '/ships/', {str(enemy_player + '_hit'): new_hit}, auth_token)
    if check_game_ended(new_hit):
        data = {'winner': id, 'status': 'ENDED'}
        Firebase.patch('/games/' + str(game_id), data, auth_token)
    return message_types.VoidMessage()


def calculate_hits(shoot_positions, enemy_ships, enemy_hit):
    hit = enemy_hit
    is_hit = False
    position_hit= []
    for index, ship in enumerate(enemy_ships):
        for positions in ship:
            for idx, position in enumerate(ship[positions]):
                if position in shoot_positions:
                    if hit[index][positions][idx] == False:
                        hit[index][positions][idx] = True
                        position_hit.append(position)
                        is_hit = True
    return is_hit, hit, position_hit


def check_game_ended(hit):
    for ship in hit:
        for positions in ship:
            for position in ship[positions]:
                if position is False:
                    return False
    return True
