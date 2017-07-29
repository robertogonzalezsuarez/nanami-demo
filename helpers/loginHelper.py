# -*- coding: utf-8 -*-
import logging

import endpoints

from messages.loginMessage import LoginValidationErrorMessage, LoginResponseMessage
from models.profile import Profile


def login(request):
    validation_errors = []
    if request.name == "" or request.name is None:
        raise endpoints.BadRequestException('Debes indicar un nombre de perfil')
    profile = Profile.query(Profile.name == request.name).get()
    if profile:
        validation_errors.append(LoginValidationErrorMessage(field='Nombre', validation_error='Ya existe'))
        return LoginResponseMessage(validation_errors=validation_errors, response_code=400)
    else:
        profile = Profile()
        profile.name = request.name
        key = profile.put()
        return LoginResponseMessage(id=str(key.id()), response_code=200, validation_errors=[])
