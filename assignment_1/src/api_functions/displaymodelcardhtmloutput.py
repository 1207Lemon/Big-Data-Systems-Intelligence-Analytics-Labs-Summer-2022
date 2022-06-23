import os
# @Description: show model card info Html page
# @Author: Cheng Wang
# @UpdateDate: 6/17/2022
def displayModelCardHtmlOutput():
    try:
        abs_path = os.path.dirname(os.path.dirname(os.path.dirname((os.path.abspath(__file__)))))
        html_file_path= abs_path + "\\notebooks\\model_card\\Team_2__Scikit_Learn_Model_Card_Toolkit_Demo.html"

        HtmlFile = open(html_file_path, 'r', encoding='utf-8')
        response = HtmlFile.read()
    except:
        print("There are some error in this function.")

    return response