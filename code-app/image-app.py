#!/usr/bin/env python3
import boto3
import json
import urllib.request
import os

def lambda_handler(event, context):
    # get filename and url for payload
    file_name = event['filename']
    original_url = event['url']
    ACCESS_KEY = os.environ['ACCESS_KEY']
    SECRET_KEY = os.environ['SECRET_KEY']
    bucket_name = os.environ['bucket_name']
    DBtable = os.environ['DBtable']
    current_region = os.environ['current_region']
    tmp_file_name = '/tmp/' + file_name
    s3_session = session = boto3.session.Session(aws_access_key_id=ACCESS_KEY,
              aws_secret_access_key=SECRET_KEY)
    
    get_image_from_url(tmp_file_name, original_url)
    upload_img_to_s3(bucket_name, current_region, tmp_file_name, file_name, s3_session)
    timestamp = get_key_timestamp(bucket_name, file_name, s3_session)
    s3_path = 's3://' +  bucket_name + '/' + file_name
    #print(file_name, original_url, s3_path, timestamp)
    
    put_img_data_to_db(file_name, original_url, s3_path, str(timestamp), s3_session)
    images_list = list_objects_in_s3(bucket_name, s3_session)
    
    return json.dumps(images_list)
    #return json.dumps({ "Filename": file_name, 
    #            "Original URL": original_url,
    #            "S3 Path": s3_path,
    #            "Timestamp": str(timestamp)})

def get_image_from_url(file_name, image_url):
    urllib.request.urlretrieve(image_url, file_name)

def upload_img_to_s3(bucket_name, region, tmp_file_name, file_name, s3_session):
    s3_resource = s3_session.resource('s3')
    s3_resource.Bucket(bucket_name).upload_file(
        Filename=tmp_file_name, Key=file_name, ExtraArgs={'ACL':'public-read'})
    
def list_objects_in_s3(bucket_name, s3_session):
    s3_resource = s3_session.resource('s3')
    bucket = s3_resource.Bucket(name=bucket_name)
    img_list = []
    for obj in bucket.objects.all():
        #print(obj.key)
        img_list.append(obj.key)
    return img_list

def get_key_timestamp(bucket_name, file_name, s3_session):
    s3_resource = s3_session.resource('s3')
    bucket = s3_resource.Bucket(name=bucket_name)
    for obj in bucket.objects.all():
        print(obj)
        if obj.key == file_name:
            return obj.last_modified
        else:
            continue
    return None

def put_img_data_to_db(file_name, original_url, s3_path, timestamp, DBtable,s3_session):
     db_resource = s3_session.resource('dynamodb')
     table = db_resource.Table(DBtable)
     print(table.table_status)
     table.put_item(Item= {'FileName': file_name,'OriginalUrl': original_url,
                         'S3_Path': s3_path, 'Timestamp': timestamp })
