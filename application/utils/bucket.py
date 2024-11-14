from django.conf import settings
from boto3 import client


class BucketClient:
    def __init__(self, folder):
        self.bucket_folder = folder
        self.bucket_name = settings.S3_BUCKET_NAME
        self.bucket_region = settings.S3_BUCKET_REGION
        self.aws_access_key = settings.AWS_ACCESS_KEY
        self.aws_access_secret = settings.AWS_ACCESS_SECRET

        self.bucket_client = client(
            's3',
            region_name=self.bucket_region,
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_access_secret
        )

        self.__url = f'https://{self.bucket_name}.s3.{self.bucket_region}.amazonaws.com'

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/upload_fileobj.html
    def upload_object(self, filename, stream):
        try:
            object_folder = f'{self.bucket_folder}/{filename}'
            self.bucket_client.upload_fileobj(
                stream, self.bucket_name, object_folder,
                ExtraArgs={'ACL': 'public-read'}
            )
            return f'{self.__url}/{object_folder}'
        except Exception as e:
            print(f'Bucket error -> {str(e)}')
