from alexi import db
from alexi.speechlet_helper import build_response

class Intent(object):

    def handle(self, request):
        raise NotImplementedError("You need to implement 'handle'!")


class GetSpeedIntent(Intent):

    def handle(self, request):
        row = db.get_latest_row()
        return build_response("{} kilometers per hour".format(row['speed']))


class IntentHandler(object):

    def handle(self, request):

        intent_name = request['intent']['name']

        for intent in Intent.__subclasses__():
            if intent.__name__ == intent_name:
                return intent().handle(request)

        raise ValueError("Unsupported intent!")
