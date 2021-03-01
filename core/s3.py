import os
import boto3
from botocore.exceptions import ClientError
import logging

FILE_BUCKET = 'anchorloans-test'

client = boto3.client('s3', aws_access_key_id=os.getenv('S3_ACCESS_KEY'), aws_secret_access_key=os.getenv('S3_SECRET_ACCESS_KEY'))


def upload_to_s3(file, key, folder):
	try:
		response = client.upload_fileobj(file, FILE_BUCKET, f'{folder}/{key}')
		print('ok')
	except ClientError as e:
		logging.error(e)
		return False
	return True


def get_s3_url(key, folder):
	return f'https://{FILE_BUCKET}.s3-us-west-2.amazonaws.com/{folder}/{key}'


def generate_s3_url(key, folder):
	url = client.generate_presigned_url('get_object',
		Params={
			'Bucket': FILE_BUCKET,
			'Key': folder + '/' + key
		}, ExpiresIn=86400) # 604800
	return url