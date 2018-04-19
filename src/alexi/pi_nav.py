import boto3
import json

def _iot():
    return boto3.client('iot-data')

def _publish(topic, payload):
    return _iot().publish(
        topic=topic,
        qos=1,
        payload=json.dumps(payload)
    )

def navigate_to(latitude, longitude):
    _publish("/pi-nav/navigate-to", {
        "latitude": latitude,
        "longitude": longitude,
    })

def switch_page(page):
    _publish("/pi-nav/action", {
        "page": page
    })

def shutdown():
    _publish("/pi-nav/shutdown", {})