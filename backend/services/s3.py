import boto3
from io import BytesIO
from settings import settings
from fastapi.exceptions import HTTPException as HttpException
from fastapi import UploadFile
from botocore.exceptions import ClientError
from repository.uploads import UploadsRepository as Uploads
import traceback
import json
from uuid import uuid4
import time
from loguru import logger


class S3Service:
    def __init__(self, db, folder_path, session=None):
        if session is None:
            session = {}
        self.bucket_name = "dev-bill-infraweigh"
        self.org_id = session.get("org_id", None)
        self.session = session
        self.client = boto3.client('s3',
                                   aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                   aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                   )
        self.repo = Uploads(db, session)
        self.db = db
        self.folder_path = folder_path

    def upload(self, file: UploadFile):
        try:
            folder_path = self.folder_path + "/" + file.filename
            self.client.upload_fileobj(
                file.file, self.bucket_name, folder_path)

            return self.repo.create({
                "name": file.filename,
                "bucket": self.bucket_name,
                "file_name": folder_path,
            })
        except ClientError as e:
            traceback.print_exc()
            return False

    def upload_obj(self, buffer, file_name):
        try:
            folder_path = self.folder_path + "/" + file_name
            self.client.put_object(
                Bucket=self.bucket_name, Key=folder_path, Body=buffer)

            return self.repo.create({
                "name": file_name,
                "bucket": self.bucket_name,
                "file_name": folder_path,
            })
        except ClientError as e:
            traceback.print_exc()
            return False

    def download(self, id):
        try:
            file = self.repo.findOne(id)
            response = self.client.generate_presigned_url('get_object',
                                                          Params={'Bucket': file.bucket,
                                                                  'Key': file.file_name},
                                                          ExpiresIn=3600)
            return response
        except ClientError as e:
            return False

    def get_file(self, id):
        start_time = time.time()
        upload_entry = self.repo.findOne(id)
        s3_object = self.client.get_object(
            Bucket=self.bucket_name, Key=upload_entry.file_name)
        end_time = time.time()
        start_time = time.time()
        csv_content = s3_object['Body'].read()
        execution_time = end_time - start_time
        logger.info(
            f"Downloaded file from S3 in {execution_time} seconds")
        logger.info("Preprocessing file")
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(
            f"Preprocessed file in {execution_time} seconds")
        return BytesIO(csv_content)

    def upload_json(self, data, file_name):
        try:
            start_time = time.time()
            file_path = self.folder_path + "/" + str(uuid4()) + file_name
            self.client.put_object(Body=json.dumps(data, indent=2, default=str), Bucket=self.bucket_name,
                                   Key=file_path)
            resp = self.repo.create({
                "name": file_name,
                "bucket": self.bucket_name,
                "file_name": file_path,
            })
            end_time = time.time()
            execution_time = end_time - start_time
            logger.info(
                f"Uploaded file to S3 in {execution_time} seconds")
            return resp
        except ClientError as e:
            traceback.print_exc()
            return False
