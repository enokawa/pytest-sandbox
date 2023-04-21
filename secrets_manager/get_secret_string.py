import json
import boto3

def get_secret_string() -> dict:
    client = boto3.client('secretsmanager', region_name="ap-northeast-1")
    response = client.get_secret_value(
        SecretId='sample/pytest'
    )
    secret_string: str = response["SecretString"]

    return json.loads(secret_string)
