import boto3, botocore
import os
from werkzeug.utils import secure_filename
import uuid

AWS_BUCKET_NAME = "bakingbuddy"
AWS_ACCESS_KEY = "AKIATNCRJ6QZ3JJW3TM4"
AWS_SECRET_ACCESS_KEY = "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"
AWS_DOMAIN = "https://bakingbuddy.s3.us-west-2.amazonaws.com"

s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)


def upload_file_to_s3(file):
    name = str(uuid.uuid4()) + secure_filename(file.filename)
    try:
        s3.upload_fileobj(
            file,
            AWS_BUCKET_NAME,
            name,
            ExtraArgs={
                "ACL": "public-read",
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return ""

    # after upload file to s3 bucket, return filename of the uploaded file
    return AWS_DOMAIN + "/" + name
