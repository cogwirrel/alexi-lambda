import sys
import arrow
import boto3
import uuid

TRACKING_DOMAIN = 'AlexiData'
EVENTS_DOMAIN = 'AlexiEventData'

def _db():
    return boto3.client('sdb')


def _attributes_to_dict(attributes):
    return {x['Name']: x['Value'] for x in attributes}

def _get_attributes(result):
    all_attributes = _get_all_attributes(result)
    if len(all_attributes) > 0:
        return all_attributes[0]
    else:
        return {}

def _get_all_attributes(result):
    if 'Items' in result:
        return map(lambda x: _attributes_to_dict(x['Attributes']), result['Items'])
    else:
        return []

def _paged_select(expr, token=None):
    params = {
        'SelectExpression': expr,
    }

    if token is not None:
        params['NextToken'] = token

    query_result = _db().select(**params)
    results = _get_all_attributes(query_result)

    if 'NextToken' in query_result:
        results += _paged_select(expr, token=query_result['NextToken'])

    return results

def _get_latest_event_timestamp(event):
    result = _get_attributes(_db().select(
        SelectExpression="select * from {domain} where event = '{event}' and timestamp >= '{after}' order by timestamp desc limit 1".format(
            domain=EVENTS_DOMAIN,
            after=arrow.get('2017-01-01T00:00Z').isoformat(),
            event=event
        )
    ))

    print result

    return arrow.get(result.get('timestamp', '2017-01-01T00:00Z')).isoformat()

def _get_reset_timestamp():
    return _get_latest_event_timestamp('reset_statistics')

def _get_journey_start_timestamp():
    return _get_latest_event_timestamp('start_journey')

def get_latest_tracking_entry():
    return _get_attributes(_db().select(
        SelectExpression="select * from {domain} where timestamp >= '{after}' order by timestamp desc limit 1".format(
            domain=TRACKING_DOMAIN,
            after=arrow.utcnow().replace(days=-1).isoformat()
        )
    ))

def get_speed():
    # Get the latest entry in the last day
    result = get_latest_tracking_entry()
    return result.get('speed', None)

def get_location():
    result = get_latest_tracking_entry()
    return result.get('latitude', None), result.get('longitude', None)


def get_all_locations_since_reset():
    after = _get_reset_timestamp()
    return _paged_select("select * from {domain} where timestamp >= '{after}' order by timestamp asc".format(
        domain=TRACKING_DOMAIN,
        after=after
    ))

def get_current_journey():
    after = _get_journey_start_timestamp()
    return _paged_select("select * from {domain} where timestamp >= '{after}' order by timestamp asc".format(
        domain=TRACKING_DOMAIN,
        after=after
    ))

def get_top_speed():
    after = _get_reset_timestamp()

    result = _get_attributes(_db().select(
        SelectExpression="select * from {domain} where timestamp >= '{after}' and speed >= '0' and speed != 'nan' order by speed desc limit 1".format(
            domain=TRACKING_DOMAIN,
            after=after
        )
    ))

    return result.get('speed', None)

def reset_statistics():
    timestamp = arrow.utcnow()

    _db().put_attributes(
        DomainName=EVENTS_DOMAIN,
        ItemName=str(uuid.uuid4()),
        Attributes=[
            {
                'Name': 'timestamp',
                'Value': timestamp.isoformat(),
                'Replace': True
            },
            {
                'Name': 'event',
                'Value': 'reset_statistics',
                'Replace': True
            }
        ]
    )

def set_speed(speed):
    timestamp = arrow.utcnow()

    _db().put_attributes(
        DomainName=TRACKING_DOMAIN,
        ItemName=str(uuid.uuid4()),
        Attributes=[
            {
                'Name': 'timestamp',
                'Value': timestamp.isoformat(),
                'Replace': True
            },
            {
                'Name': 'speed',
                'Value': str(speed),
                'Replace': True
            }
        ]
    )
