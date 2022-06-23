import os
# @Description: get HTML home page
# @Author: Cheng Wang
# @UpdateDate: 6/12/2022

def getHomePage():
    try:
        abs_path = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
        html_path = abs_path+"\\index.html"

        html_file = open(html_path, 'r', encoding='utf-8')
        response = html_file.read()
    except:
        print("There are some error in this function.")

    return response