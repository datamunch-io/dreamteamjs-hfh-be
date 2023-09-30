import os
from enum import Enum

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


def create_posting(**kwargs):
    '''
    Inbound params:
    - name: str Posting name
    - donator_name: str Donator's name (individual or business)
    - addr_1: str
    - addr_2: str <optional>
    - city: str
    - state: str
    - zip: str
    - dollar_val: float
    - image_uri: string - GCS URI to donation image
    :param kwargs:
    :return:
    '''
    conn = get_connection()
    name = kwargs.get('name')
    donator_name = kwargs.get('donator_name')
    addr_1 = kwargs.get('addr_1')
    addr_2 = kwargs.get('addr_2', '')
    description = kwargs.get('description')
    city = kwargs.get('city')
    state = kwargs.get('state')
    zip = kwargs.get('zip')
    dollar_value = kwargs.get('dollar_value')
    image_uri = kwargs.get('image_uri')
    insert_sql = f"""
        INSERT INTO posts (name, donator_name, addr_1, addr_2, city, state, zip, status_id, dollar_val, description, gcs_image)
        VALUES ('{name}', '{donator_name}', '{addr_1}', '{addr_2}', '{city}', '{state}', '{zip}', {Status.POSTED},
        {dollar_value}, '{description}','{image_uri}')
    """

    pool = sa.create_engine(
        "mysql+pymysql://",
        creator=conn
    )

    with pool.connect() as db_conn:
        result = db_conn.execute(insert_sql).fetchall()

    conn.close()


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
