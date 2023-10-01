import os
import json
from enum import Enum

import functions_framework
from google.cloud.sql.connector import Connector, IPTypes
from dotenv import load_dotenv
import sqlalchemy as sa
import pymysql


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
    db = os.environ.get('DB')
    connection = connector.connect(
        f"{PROJECT_ID}:{REGION}:{INSTANCE}",
        "pymysql",
        user=user,
        password=password,
        db=db
    )

    return connection


def get_postings(**kwargs):
    only_certified = bool(int(kwargs.get('certified', False)))
    conn = get_connection()
    if only_certified:
        sql = f"""
            SELECT * FROM post
            WHERE status_id = {Status.CERTIFIED.value};
        """
    else:
        sql = f"""
            SELECT * FROM post;
        """

    sql = sa.text(sql)

    pool = sa.create_engine(
        "mysql+pymysql://",
        creator=get_connection
    )

    with pool.connect() as db_conn:
        result = db_conn.execute(sql).all()

    results = []
    for row in result:
        row_ = {
            'id': row.id,
            'created_at': row.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'description': row.description,
            'addr_1': row.addr_1,
            'addr_2': row.addr_2,
            'city': row.city,
            'state': row.state,
            'zip': row.zip,
            'status_id': row.status_id,
            'image_uri': row.image_uri
        }
        results.append(row_)

    conn.close()
    return results


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

    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    request_json = request.get_json(silent=True)
    only_certified = request_json.get('certified', False)
    return (get_postings(certified=only_certified), 200, headers)
