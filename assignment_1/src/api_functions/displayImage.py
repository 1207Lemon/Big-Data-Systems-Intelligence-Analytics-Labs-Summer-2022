import os
import json
from json import load
from boto3 import client
import boto3
import base64
import random
# @Description: display 5 random images
# @Author: Cheng Wang
# @UpdateDate: 6/12/2022
def showRandomImg():
    try:
        data1="""
            <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta http-equiv="X-UA-Compatible" content="IE=edge">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Assignment 1</title>
                </head>
                <body>
                    <h1>Military Aircraft Detection version 7</h1>
                    <h2>Random 5 images Display</h2>
        """

        html_img=""

        file_list = getNumRandomImageFileNames(5)
        for i in range(len(file_list)):
            body = getS3BucketBody(file_list[i])
            img_base64_data = base64.b64encode(body)
            img_data = img_base64_data.decode('utf-8')

            html_img= html_img + '<img src="data:image/png;base64,' + img_data +'"/>'
        
        data2="""     
                </body>
            </html>
        """
        response=data1+html_img+data2
    except:
        print("There are some error in this function.")
    return response




def getS3BucketBody(imgName):
    
    
    
    #check image
    
    key = 'image/' + imgName + '.jpg'
    
    abs_path = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
    csv_path = abs_path+"\\credentials\\aws_s3_credentials.json"

    credentials = json.load(open(csv_path))

    s3_resource = boto3.client(
        service_name=credentials['service_name'],
        region_name=credentials['region_name'],
        aws_access_key_id=credentials['aws_access_key_id'],
        aws_secret_access_key=credentials['aws_secret_access_key'])


    bucket = credentials['aws_s3_bucket_name']

    obj = s3_resource.get_object(Bucket = bucket , Key = key)
    body = obj['Body'].read()
    return body




def getNumRandomImageFileNames(num):
    if(num > 9):
        return {"error": "You should give a number which is less than 10!"}

    key = 'csv/combined.csv'
    abs_path = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
    csv_path = abs_path+"\\credentials\\aws_s3_credentials.json"

    credentials = json.load(open(csv_path))

    s3_resource = boto3.client(
        service_name=credentials['service_name'],
        region_name=credentials['region_name'],
        aws_access_key_id=credentials['aws_access_key_id'],
        aws_secret_access_key=credentials['aws_secret_access_key'])


    bucket = credentials['aws_s3_bucket_name']

    obj = s3_resource.get_object(Bucket = bucket , Key = key)
    body_str = obj['Body'].read().decode()

    csv_header_value_list = body_str.split() # split body into 1 list (contain csv headers and values) header=str->  csv_header_value_list[0]        value=string

    fileName_list = [None] * num
    
    randNum = random.randint(0, 350-num)
        
    
    index_no = 0
    for i in range(len(csv_header_value_list)):
        if(i > randNum):                       
            csv_header_value_list[i] = csv_header_value_list[i].split(',') #  slipt value list ','
            
            if(csv_header_value_list[i][0] != csv_header_value_list[i-1][0]):
                if(index_no == num):
                    break
                fileName_list[index_no] = csv_header_value_list[i][0]
                index_no += 1
    
    
    return fileName_list