import pytest
from api_test import *

def test_assistant(chat_assistant):
    """Test general chat assistant method."""
    assert chat_assistant.status_code == 200

def test_file_upload(upload_File):
    """Test general File Upload method."""
    token, session_id, file_id = upload_File

def test_insights_bigquery(insights_bq):
    """Test insights bigquery method."""
    assert insights_bq.status_code == 200

def test_insights_file(insights_file):
    """Test insights File method."""
    assert insights_file.status_code == 200