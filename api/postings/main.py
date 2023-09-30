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

    conn.close()
    return [json.dumps([dict(row._mapping) for row in result], default=str)]


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
    return get_postings(certified=only_certified)
