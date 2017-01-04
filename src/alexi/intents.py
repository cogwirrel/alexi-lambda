from alexi import db
from alexi.speechlet_helper import build_response, get_slots

class Intent(object):

    def handle(self, request):
        raise NotImplementedError("You need to implement 'handle'!")


class GetSpeedIntent(Intent):

    def handle(self, request):
        speed = db.get_speed()
        return build_response("{} kilometers per hour".format(speed))


class CreateTableIntent(Intent):

    def handle(self, request):
        try:
            db.create_table()
            return build_response("done")
        except Exception as e:
            return build_response("error: {}".format(str(e)))


class SetSpeedIntent(Intent):

    def handle(self, request):
        slots = get_slots(request)
        db.set_speed(float(slots['speed']))
        return build_response("Your speed is {} kilometers per hour".format(slots['speed']))


class SelectAllIntent(Intent):

    def handle(self, request):
        return build_response(repr(db.select_all()))


class IntentHandler(object):

    def handle(self, request):

        intent_name = request['intent']['name']

        for intent in Intent.__subclasses__():
            if intent.__name__ == intent_name:
                return intent().handle(request)

        raise ValueError("Unsupported intent!")
