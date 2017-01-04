import sys
import arrow
import boto3
import uuid

DOMAIN = 'AlexiData'

def _db():
    return boto3.client('sdb')


def _attributes_to_dict(attributes):
    return {x['Name']: x['Value'] for x in attributes}


def get_speed():
    # Get the latest entry in the last day
    result = _db().select(
        SelectExpression="select * from {domain} where timestamp >= '{after}' order by timestamp desc limit 1".format(
            domain=DOMAIN,
            after=arrow.utcnow().replace(days=-1).isoformat()
        )
    )

    if len(result['Items']) > 0:
        return _attributes_to_dict(result['Items'][0]['Attributes'])['speed']
    else:
        return None


def create_table():
    _db().create_domain(
        DomainName=DOMAIN
    )


def set_speed(speed):
    timestamp = arrow.utcnow()

    _db().put_attributes(
        DomainName=DOMAIN,
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
