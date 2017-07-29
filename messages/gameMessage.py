from protorpc import messages


class ShipMessage(messages.Message):
    name = messages.StringField(1, required=True)
    positions = messages.StringField(2, repeated=True)


class ShipsMessage(messages.Message):
    id = messages.StringField(1, required=True)
    game = messages.StringField(2, required=True)
    ships = messages.MessageField(ShipMessage, 3, repeated=True)


class GameMessage(messages.Message):
    game = messages.StringField(1, required=True)


class GameIdMessage(messages.Message):
    game = messages.StringField(1, required=True)
    id = messages.StringField(2, required=True)
