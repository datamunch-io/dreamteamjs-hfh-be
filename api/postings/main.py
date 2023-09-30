import os
from enum import Enum
import datetime
import uuid

import functions_framework
from google.cloud.sql.connector import Connector, IPTypes
from dotenv import load_dotenv
import sqlalchemy as sa


load_dotenv()

PROJECT_ID = os.environ.get('PROJECT_ID')
REGION = os.environ.get('REGION')
INSTANCE = os.environ.get('INSTANCE')


class Status(Enum):
    POSTED = 1
    RECEIVED = 2
    CERTIFIED = 3


def get_connection():
    connector = Connector()
    user = os.environ.get('USER')
    password = os.environ.get('PASSWORD')
    connection = connector.connect(
        f"{PROJECT_ID}:{REGION}:{INSTANCE}",
        "pg8000",
        user=user,
        password=password,
        iptype=IPTypes.PUBLIC
    )

    return connection


def get_postings(**kwargs):
    only_certified = kwargs.get('certified', False)
    conn = get_connection()
    sql = """
        SELECT * FROM 
    """


@functions_framework.http
def main(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    only_certified = request_json.get('certified', False)
    request_args = request.args
    print(request_args)
    print(request_json)

    if request_json and 'name' in request_json:
        name = request_json['name']
    elif request_args and 'name' in request_args:
        name = request_args['name']
    else:
        name = 'World'
    return 'Hello {}!'.format(name)