from alexi import db, pi_nav
from alexi.geo import geo
from alexi.speechlet_helper import build_response, get_slots
import arrow

ADDRESS_COMPONENTS = ['house_number', 'house_letter', 'street', 'suburb', 'city', 'postcode']

class Intent(object):

    def handle(self, request):
        raise NotImplementedError("You need to implement 'handle'!")


class GetSpeedIntent(Intent):

    def handle(self, request):
        speed = db.get_speed()

        if speed is not None:
            return build_response("{:.0f} kilometers per hour".format(round(float(speed))))
        else:
            return build_response("I don't know your speed")


class GetTopSpeedIntent(Intent):
    def handle(self, request):
        top_speed = db.get_top_speed()

        if top_speed is not None:
            return build_response("{:.0f} kilometers per hour".format(round(float(top_speed))))
        else:
            return build_response("I don't know your top speed")


class GetLocationIntent(Intent):
    def handle(self, request):
        latitude, longitude = db.get_location()

        address = geo.reverse(latitude, longitude)

        return build_response("{}".format(address))


class ResetStatisticsIntent(Intent):
    def handle(self, request):
        db.reset_statistics()
        return build_response("Done!")


class TotalDistanceIntent(Intent):
    def handle(self, request):
        locations = db.get_all_locations_since_reset()
        if len(locations) > 1:
            print locations
            start_time = arrow.get(locations[0]['timestamp'])
            points = map(lambda x: (float(x['latitude']), float(x['longitude'])), locations)
            distance = geo.distance(points)
            return build_response("You've travelled {:.1f} kilometers since about {}".format(float(distance), start_time.humanize()))
        else:
            return build_response("I don't have enough data to know the distance travelled")

class CurrentJourneyIntent(Intent):
    def handle(self, request):
        locations = db.get_current_journey()
        if len(locations) > 1:
            start_time = arrow.get(locations[0]['timestamp'])
            points = map(lambda x: (float(x['latitude']), float(x['longitude'])), locations)
            distance = geo.distance(points)
            speeds = [float(x['speed']) for x in locations]
            avg_speed = sum(speeds) / len(locations)
            top_speed = max(speeds)

            speech = "You've travelled {:.1f} kilometers since about {}.".format(distance, start_time.humanize())
            speech += " Your average speed is {:.1f} kilometers per hour.".format(avg_speed)
            speech += " Your top speed is {:.1f} kilometers per hour.".format(top_speed)

            return build_response(speech)
        else:
            build_response("I'm sorry, I haven't started tracking your journey yet.")

class NavigateToIntent(Intent):

    def handle(self, request):
        slots = get_slots(request)

        input_address = ""

        for address_part in ADDRESS_COMPONENTS:
            if address_part in slots:
                input_address += "{} ".format(slots[address_part])

        latitude, longitude, address = geo.geocode(input_address)

        pi_nav.navigate_to(latitude, longitude)

        return build_response("I've set a course for {}".format(address))


class ShutdownIntent(Intent):
    def handle(self, request):
        pi_nav.shutdown()
        return build_response("I've shut down the raspberry pi!")


class IntentHandler(object):

    def handle(self, request):

        intent_name = request['intent']['name']

        for intent in Intent.__subclasses__():
            if intent.__name__ == intent_name:
                return intent().handle(request)

        raise ValueError("Unsupported intent!")
