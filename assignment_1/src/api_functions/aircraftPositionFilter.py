import os
import json
from json import load
from boto3 import client
import boto3
# @Description: take aircraft bounding box as a input, out put files which have the same bounding box area
# @Author: Cheng Wang
# @UpdateDate: 6/12/2022
def getAircraftPositionFilterResult(xmin=0,ymin=0,xmax=0,ymax=0):
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
        inner_index_num = csv_header_value_list[0].split(',')   # header 0-7 [0] file_name
        index_no = 0
        result={}

        # filename="4a042db1cef213a1ed865422e6355f76"
        # className=""

        for i in range(len(csv_header_value_list)):
            if(i > 0):
                index_no += 1 #?   +1 record(key+value)
                            
                header_list = csv_header_value_list[0].split(',') # split key(header) list
                        
                csv_header_value_list[i] = csv_header_value_list[i].split(',') #  slipt value list ','
                
        
                
                
                #xmin ymin xmax ymax check
                if(xmax == 0):
                    xmax = int(csv_header_value_list[i][1]) #width
                if(ymax == 0):
                    ymax = int(csv_header_value_list[i][2]) #height

                xmin_check = xmin <= int(csv_header_value_list[i][4]) < xmax
                xmax_check = xmin < int(csv_header_value_list[i][6]) <= xmax
                ymin_check = ymin <= int(csv_header_value_list[i][5]) < ymax
                ymax_check = ymin < int(csv_header_value_list[i][7]) <= ymax
                
            
                if(xmin_check and xmax_check and ymin_check and ymax_check):
                    result[str(index_no)] = {}
                    for j in range(len(inner_index_num)): #? 8 elements
                        result[str((index_no))][header_list[j]] = csv_header_value_list[i][j] # i = 0      |      j = 0 - 7
    except:
        print("There are some error in this function.")
            
    return result


