from urllib.parse import urljoin
from dotenv import load_dotenv
import os

load_dotenv()

import names
import pytest
import requests
import pandas as pd
from io import BytesIO
from all_file import insight_file_excel
from all_bigquery import get_bigquery_table

basic_url = "http://127.0.0.1:5000"

login_endpoint = urljoin(basic_url, "/addworld")
upload_file_endpoint = urljoin(basic_url, "/addworld")
insights_file_endpoint = urljoin(basic_url, "/addworld")
insights_bq_endpoint = urljoin(basic_url, "/addworld")
create_session_endpoint = urljoin(basic_url, "/world/")
get_session_endpoint = urljoin(basic_url, "/world/")
chat_assistant_endpoint = urljoin(basic_url, "/world/{session_id}")


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

@pytest.fixture
def get_Token():
    user_token = os.getenv('login_token')
    return user_token

@pytest.fixture
def create_session(get_Token):
    """Creates a new session"""

    headers = {"Authorization": f"Bearer {get_Token}"}
    auth = BearerAuth(get_Token)
    data = {}
    create_session_response = requests.post(create_session_endpoint, data=data, auth=auth)
    assert create_session_response.status_code == 200
    return get_Token, create_session_response.json()["session_id"]

def chat_assistant(create_session):
    token, session_id = create_session
    chat_assistant_endpoint = chat_assistant_endpoint.format(session_id=session_id)
    data = {
        "message": "",
        "system_message": ""
    }
    auth = BearerAuth(token)
    return requests.post(chat_assistant_endpoint, data=data, auth=auth)

def translation(create_session):
    token, session_id = create_session
    chat_assistant_endpoint = chat_assistant_endpoint.format(session_id=session_id)
    data = {
        "message": "",
        "system_message": ""
    }
    auth = BearerAuth(token)
    return requests.post(chat_assistant_endpoint, data=data, auth=auth)

@pytest.fixture
def create_insight_file():
    return insight_file_excel()

@pytest.fixture
def upload_File(create_session, create_insight_file):
    """Upload a file"""
    token, session_id = create_session
    upload_file_endpoint = upload_file_endpoint + "/" + session_id
    data = {
        'file': create_insight_file,
        'metadata': {"filetype":"insight"}
    }
    auth = BearerAuth(token)
    upload_file_response = requests.post(upload_file_endpoint, data=data, auth=auth)
    assert upload_file_response.status_code == 200
    return token, session_id, upload_file_response.json()["file_id"]

@pytest.fixture
def insights_file(upload_File):
    """test insight file"""
    token, session_id, file_id = upload_File
    insights_file_endpoint = insights_file_endpoint + "/" + session_id
    data = {
        'session_id': session_id,
        'file_id': file_id,
        'message': "Hello World"
    }
    auth = BearerAuth(token)
    return requests.post(insights_file_endpoint, data=data, auth=auth)

@pytest.fixture
def create_bigquery(create_session):
    token, session_id = create_session
    return token, session_id, get_bigquery_table()

@pytest.fixture
def insights_bq(create_bigquery):
    """test insight file"""
    token, session_id, table_name = create_bigquery
    insights_bq_endpoint = insights_bq_endpoint + "/" + session_id
    data = {
        'session_id': session_id,
        'table_name': table_name,
        'message': "Hello World"
    }
    auth = BearerAuth(token)
    return requests.post(insights_bq_endpoint, data=data, auth=auth)