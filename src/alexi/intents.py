from alexi import db
from alexi.speechlet_helper import build_response, get_slots

class Intent(object):

    def handle(self, request):
        raise NotImplementedError("You need to implement 'handle'!")


class GetSpeedIntent(Intent):

    def handle(self, request):
        speed = db.get_speed()

        if speed is not None:
            return build_response("{} kilometers per hour".format(speed))
        else:
            return build_response("I don't know your speed")


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


class IntentHandler(object):

    def handle(self, request):

        intent_name = request['intent']['name']

        for intent in Intent.__subclasses__():
            if intent.__name__ == intent_name:
                return intent().handle(request)

        raise ValueError("Unsupported intent!")
