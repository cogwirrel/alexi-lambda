import sys
import pymysql
import arrow
import boto3
import os
from base64 import b64decode

def _get_decrypted_environment_variable(key):
    return os.environ[key]

    # TODO - Actually encrypt the secret stuff!
    # encrypted = os.environ[key]
    # # Decrypt code should run once and variables stored outside of the function
    # # handler so that these are decrypted once per container
    # return boto3.client('kms').decrypt(CiphertextBlob=b64decode(encrypted))['Plaintext']

DB_HOST = _get_decrypted_environment_variable('DB_HOST')
DB_PORT = int(_get_decrypted_environment_variable('DB_PORT'))
DB_NAME = _get_decrypted_environment_variable("DB_NAME")
DB_USERNAME = _get_decrypted_environment_variable("DB_USERNAME")
DB_PASSWORD = _get_decrypted_environment_variable("DB_PASSWORD")


def _db():
    return pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USERNAME, passwd=DB_PASSWORD, db=DB_NAME, connect_timeout=5)


def get_speed():
    db = _db()
    with db.cursor() as cursor:
        cursor.execute("select speed, timestamp from alexi_data order by timestamp DESC limit 1")
        return cursor.fetchone()[0]


def create_table():
    db = _db()
    with db.cursor() as cursor:
        cursor.execute("create table alexi_data (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, timestamp DATETIME NOT NULL, speed DOUBLE)")
        db.commit()


def set_speed(speed):
    timestamp = arrow.utcnow()
    db = _db()
    with db.cursor() as cursor:
        cursor.execute("insert into alexi_data (timestamp, speed) values (%s, %s)", (timestamp.format('YYYY-MM-DD HH:mm:ss'), speed))
        db.commit()


def select_all():
    db = _db()
    with db.cursor() as cursor:
        cursor.execute("select * from alexi_data order by timestamp DESC")
        return cursor.fetchall()