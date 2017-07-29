from protorpc import messages


class LoginMessage(messages.Message):
    name = messages.StringField(1, required=True)


class LoginValidationErrorMessage(messages.Message):
    field = messages.StringField(1)
    validation_error = messages.StringField(2)


class LoginResponseMessage(messages.Message):
    response_code = messages.IntegerField(1)
    id = messages.StringField(2)
    validation_errors = messages.MessageField(LoginValidationErrorMessage, 3, repeated=True)


class IdMessage(messages.Message):
    id = messages.StringField(1, required=True)