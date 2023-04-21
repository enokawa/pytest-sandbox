import json
import boto3
import pytest

from get_secret_string import get_secret_string
from moto import mock_secretsmanager

@pytest.fixture(scope="function", autouse=False)
def create_secret():
    def _create_secret(secret_name: str, secret_value: str):
      client = boto3.client('secretsmanager', region_name="ap-northeast-1")
      client.create_secret(Name=secret_name,SecretString=secret_value)
      
    return _create_secret


@mock_secretsmanager
def test_get_secret_string(create_secret, mocker):
    expected: dict = {
        "username": "admin",
        "password": "FLsr(uZoI@@Z+Aa?",
        "engine": "mysql",
        "host": "0.0.0.0",
        "port": "3306",
        "dbname": "pytest"
    }

    create_secret(secret_name="sample/pytest", secret_value=json.dumps(expected))

    mocker.patch("get_secret_string.get_secret_string", return_value=expected)

    secret_value: dict = get_secret_string()
    assert secret_value == expected
