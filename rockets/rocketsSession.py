import boto3
import os

session = boto3.Session (
    
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY',''),
    aws_secret_access_key= os.environ.get('AWS_SECRET_ACCESS_KEY',''),
    region_name= os.environ.get('ASWS_RECGION','')
)