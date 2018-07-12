from harc.consumers.ConsumeException import ConsumeException


class Consumable(object):
    def __init__(self):
        object.__init__(self)

    def action(self):
        raise ConsumeException("method not implemented")
