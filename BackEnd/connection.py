import pymysql
import boto3

from config import database, S3


def connect_db():
    return pymysql.connect(
        host=database['host'],
        port=database['port'],
        user=database['user'],
        passwd=database['passwd'],
        db=database['db'],
        charset=database['charset']
    )


def connect_s3():
    return boto3.client(
        "s3",
        aws_access_key_id=S3["ACCESS_KEY_ID"],
        aws_secret_access_key=S3["SECRET_ACCESS_KEY"]
    )
