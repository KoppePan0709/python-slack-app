import boto3

s3 = boto3.resource('s3')

bucket = s3.Bucket('box-slack-app-imagebucket')
bucket.download_file('image/logo.png','logo.png')

