import random
import string
from fastapi import FastAPI, Query, Path, Request
from typing import Union
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from log.logger import logger
import time
from pydantic import BaseModel
from pathlib import Path
import sys
import logging
from requests import request

path = str(Path(Path(__file__).parent.absolute()))
sys.path.insert(0, path)
from api_functions import getS3BucketBody
from api_functions import numAndClassNameFiltered
from api_functions import fileNameAndClassNameFiltered
from api_functions import imgSizeRangeFiltered
from api_functions import aircraftPositionFilter
from api_functions import displayPandasCsvHtmlOutput
from api_functions import displayPandasImagesHtmlOutput
from api_functions import getNumRandomImages
from api_functions import displayImage
from api_functions import returnHomePage
from api_functions import displaymodelcardhtmloutput

# setup loggers
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)  # the __name__ resolve to "main" since we are at the root of the project. 
                                      # This will get the root logger since no logger in the configuration has this name.

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Home page
@app.get("/", response_class=HTMLResponse)
async def home():
    response = returnHomePage.getHomePage()
    return response

@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")
    
    return response

# info 8 values for filter and return response
@app.get("/api/get/infoFilter/")
async def inputInfoFilterRequest(filename:Union[str,None]= Query(default="", max_length=40),
                              width:Union[int,None] = Query(default=0),
                              height:Union[int,None] = Query(default=0),
                              className:Union[str,None] = Query(default=""),
                              xmin:Union[int,None] = Query(default=0),
                              ymin:Union[int,None] = Query(default=0),
                              xmax:Union[int,None] = Query(default=0),
                              ymax:Union[int,None] = Query(default=0)):
    className = className.upper()

    response = getS3BucketBody.getS3BucketBodyInfo(filename,width,height,className,xmin,ymin,xmax,ymax) # get return response
    if(response == {}):
        logger.error("No data Found: HTTP 404")
    return  response

# fileName , class input and return response
@app.get("/api/get/fileNameAndClass/")
async def aircraftClassAndFileNameRequest(className:str,
                              filename:Union[str,None]= Query(default="", max_length=32)):
    className = className.upper()
    
    response = fileNameAndClassNameFiltered.getFileNameClassNameFilteredResult(className,filename) # get return response
    
    if(response == {}):
        logger.error("No data Found: HTTP 404")
        
    
    return  response

# (width , weight) range and get response
@app.get("/api/get/imgSizeRange/")
async def imgSzieRangeRequest(width:Union[int,None] = Query(default=0),
                              height:Union[int,None] = Query(default=0)):
    
    response = imgSizeRangeFiltered.getimgSizeRangeFilteredResult(width,height) # get return response
    
    if(response == {}):
        logger.error("No data Found: HTTP 404")
    
    return  response

# (xmin,ymin,xmax,ymax) range and get response
@app.get("/api/get/aircraftPositionRange/")
async def aircraftPositionRequest(xmin:Union[int,None] = Query(default=0),
                                  ymin:Union[int,None] = Query(default=0),
                                  xmax:Union[int,None] = Query(default=0),
                                  ymax:Union[int,None] = Query(default=0)):
    
    response = aircraftPositionFilter.getAircraftPositionFilterResult(xmin,ymin,xmax,ymax) # get return response
    if(response == {}):
        logger.error("No data Found: HTTP 404")
    return  response

# No input value and get response(all info)
@app.get('/api/get/allInfo/')
async def getAllImgInfo():

    
    response = getS3BucketBody.getS3BucketBodyInfo() # get return response
    
    if(response == {}):
        logger.error("No data Found: HTTP 404")
    
    return response

# input aircraft Num and output all images == numbers
# option: class -> input all filtered info contain input class name
@app.get("/api/get/aircraftNumandClass/")
async def numAndClassFiteredInfoRequest(num:int,
                                         className:Union[str,None] = Query(default="")):
    
    className = className.upper()
    response = numAndClassNameFiltered.getNumAndClassFilteredResult(num,className)
    
    
    if(response == {}):
        logger.error("No data Found: HTTP 404")
        
    return  response


# get random Num images info
@app.get("/api/get/random/{num}")
async def getNumRandomImage(num: int = Path(title="Number of random aircrafts", gt=0, le=9)): 

    response =  getNumRandomImages.getNumRandomImageFileNames(num)
    
    if(response == {}):
        logger.error("No data Found: HTTP 404")
        
    return response

######################### Featured API for display #########################

# display pandas csv info html output
@app.get("/pandas/html/csv/", response_class=HTMLResponse)
async def getPandasCsvOutputHtmlPage():


    response = displayPandasCsvHtmlOutput.getPandasProfilingCsvHtmlOutput()

    if(response == {}):
        logger.error("No data Found: HTTP 404")


    return response


# display pandas profling img info html output
@app.get("/pandas/html/image/", response_class=HTMLResponse)
async def getPandasImageOutputHtmlPage():


    response = displayPandasImagesHtmlOutput.getPandasProfilingImageHtmlOutput()

    if(response == {}):
        logger.error("No data Found: HTTP 404")

    return response
    
@app.get("/modelcard/html/", response_class=HTMLResponse)
async def getModelCardOutputHtmlPage():

    response = displaymodelcardhtmloutput.displayModelCardHtmlOutput()

    if(response == {}):
        logger.error("No data Found: HTTP 404")

    return response

#Todo
# display random image and its info
@app.get("/display/image/", response_class=HTMLResponse)
async def displayImageInHTML():

    return displayImage.showRandomImg()


# @Description: input basemodel
# @Author: Cheng Wang
# @UpdateDate: 6/13/2022
class csvInfo(BaseModel):
    #description: Union[str, None] = None
    #price: float
    #tax: Union[float, None] = None
    fileName : str=None
    width : int=None
    height : int=None
    className : str # 飞机种类的 class 为 python 内置关键字 需要转换
    xmin : int=None
    ymin : int=None
    xmax : int=None
    ymax : int=None
    base64 : str=None
    RGB : dict=None
    valid_width : int=None
    valid_height : int=None
    fileSize : str=None
    aircraft_more_than_1 : bool=None
    aircraft_num : int=None
