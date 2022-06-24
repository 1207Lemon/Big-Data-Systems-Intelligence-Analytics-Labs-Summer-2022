#Todo
import os
import json
from json import load
from boto3 import client
import boto3
# @Description: take integer number and class name as input, return same amount of files that have that specific class name
# @Author: Cheng Wang
# @UpdateDate: 6/12/2022

def getNumAndClassFilteredResult(num,className=""):
    try:
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

        index_no = 0
        result={}

        count_num = 1
        for i in range(len(csv_header_value_list)):
            if(i > 0):  # ignore header list, all left are aircraft info
                

                header_list = csv_header_value_list[0].split(',')  # split key(header) list

                csv_header_value_list[i] = csv_header_value_list[i].split(',')  # slipt value list ','



                if(csv_header_value_list[i][0] == csv_header_value_list[i-1][0]):  # a a b
                    if(className == '' or className == csv_header_value_list[i][3]):
                        count_num += 1  # + 1 record
                        # result[str(index_no)][header_list[3]] = {}
                        # index1 = "class" + str(a + 1)
                        # for a in range(len(csv_header_value_list)):
                        #     result[str(index_no)]["class"][index1] = csv_header_value_list[a][3]

                else:
                    if(count_num == num and i-1 != 0):
                        result[str(index_no)] = {}
                        result[str(index_no)][header_list[0]] = csv_header_value_list[i-1][0]
                        result[str(index_no)][header_list[3]] = className
                        result[str(index_no)]["count"]=count_num
                            
                        count_num = 1
                    else:
                        count_num = 1
                        continue
                index_no += 1  # ?   +1 record(key+value)
    except:
        print("There are some error in this function.")      
    return result  