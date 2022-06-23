import os
import json
from json import load
from boto3 import client
import boto3
import random
from api_functions import fileNameFIltered
# @Description: take a integer number as input, output the infomation about the given number of images
# @Author: Cheng Wang
# @UpdateDate: 6/12/2022
def getNumRandomImageFileNames(num:int):
    try:
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
        
        
        result = {}
        for i in range(len(fileName_list)):
            result["image NO." + str(i+1)] = fileNameFIltered.getFileNameCsvInfo(fileName_list[i])
    except:
        print("There are some error in this function.")
    return result


# if __name__ == '__main__':
#     try:
#         print(getNumRandomImageFileNames(dfasdf))

#     except NameError:
#         print("Please input a correct file name!")

