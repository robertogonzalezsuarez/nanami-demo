from protorpc import messages


class ShootMessage(messages.Message):
    positions = messages.StringField(1, repeated=True)
    game = messages.StringField(2, required=True)
    id = messages.StringField(3, required=True)