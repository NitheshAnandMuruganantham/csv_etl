from dotenv import load_dotenv
import os
import boto3
from botocore.exceptions import ClientError
import json

app_config = {}


keys = ["DATABASE_URL", "AUTH_SECRET", "AUTH_ALGORITHM", "REDIS_URL",
        "REDIS_PASSWORD", "REDIS_DB", "REDIS_PORT", "SENDINBLUE_API_KEY", "ACCESS_KEY_ID",
        "SECRET_ACCESS_KEY", "API_DOMAIN", "APP_DOMAIN_1", "APP_DOMAIN_2", "SUPERTOKENS_URL",
        "SUPERTOKENS_API_KEY", "ALGOLIA_APP_ID", "ALGOLIA_API_KEY", "TWILIO_ACCOUNT_SID",
        "TWILIO_AUTH_TOKEN", "TWILIO_PHONE_NUMBER", "SUPERTOKENS_SMS_TOKEN", "MONGO_URL"]


if (os.path.exists('.env')):
    load_dotenv(".env")
    print("Loaded .env file")


def bootstrap_config():
    if (os.getenv("ENV") != "production"):
        local_config()
    else:
        prod_config()


def prod_config():
    print("Loading prod config")
    try:
        client = boto3.client('secretsmanager', region_name='us-east-1', aws_access_key_id=os.getenv("ACCESS_KEY_ID"),
                              aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"))
        get_secret_value_response = client.get_secret_value(
            SecretId="prod/infraweigh/config"
        )
    except ClientError as e:
        print(e.response['Error']['Code'])
        raise Exception("Error fetching config from AWS Secrets Manager")

    secret = get_secret_value_response['SecretString']
    secret = json.loads(secret)
    for key in keys:
        app_config[key] = secret.get(key, None)


def local_config():
    print("Loading local config")
    for key in keys:
        app_config[key] = os.getenv(key, None)
