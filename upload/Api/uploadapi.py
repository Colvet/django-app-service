import logging
import os
from datetime import datetime

import pandas as pd
import pymongo
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from upload.analytics import MakeSummary as ms
import json

logger = logging.getLogger(__name__)

## mongodb 수정해줘야댐
client = pymongo.MongoClient('mongo', 27017)
db = client.k8s_mongodb
# db = client.sixthsense
collection = db.SummaryData


@csrf_exempt
def test(request):
    cursor = collection.find({})
    responsedata=[]
    print("테스트 요청 받음")
    print(logger.warning("워닝"))
    print(logger.debug("디버"))
    print(logger.info("안포"))
    logger.warning("후........")
    logger.info("mongo test")
    logger.debug("테스트 요청 받음")
    for cu in cursor:
        del cu['_id']
        responsedata.append(cu)

    return HttpResponse(json.dumps(responsedata), status=200)
@csrf_exempt
def upload_file(request):
    print("????????????????????????????????????????")
    logger.debug("upload post요청")
    if request.method == 'POST':
        logger.debug("포스트로 받음")
        uploadFile = request.FILES['files']
        logger.debug(uploadFile)

        logger.debug(uploadFile)

        print(request.POST['userName'])
        logger.debug(request.POST['userName'])

        print("csv파일 확인작")
        if uploadFile.name.find('csv') < 0:
            message = "파일형식이 잘못되었습니다"
            logger.info(message)
            return HttpResponse(status=500)

        else:
            print("csv파일 읽기 시작")
            csv_file = pd.read_csv(uploadFile, encoding='utf8')
            logger.info("다읽음")
            print("다읽음")

            print("df로 변환 작업")
            df = pd.DataFrame(csv_file)
            time_now = datetime.now().timestamp()
            userName = request.POST['userName']

            print("폴더 생성 시작")
            # 디렉토리 저장 주소 설정
            if not (os.path.isdir('/usr/src/app/data/' + userName)):
                print('디렉톨 ㅣ없다 !@#!@#@!#!@#!@#!@#!@#!@')
                os.makedirs(os.path.join('/usr/src/app/data', userName))
            print("폴더 생성 완료")
            logger.info("test")
            save_dir = '/usr/src/app/data/' + userName
            print("null지우기 시작")
            # null 세고 지우기
            del_null_df, info = ms.analy(df)
            print("null지우기 끝")

            FileSummaryData = {
                "originalLocation": os.path.join("save_dir", str(time_now) + "_" + uploadFile.name),
                "fileName": str(time_now) + "_" + uploadFile.name,
                "userName": userName,
                "info": info
            }
            print("Db 추가 시작")
            collection.insert_one(FileSummaryData)
            print("db 추가 끝")

            print("파일 저장 시작")
            del_null_df.to_csv(os.path.join(save_dir, str(time_now) + "_" + uploadFile.name))
            print("파일 저장 끝")

            return HttpResponse(status=200)

    if request.method == "GET":
        cursor = collection.find({})
        responsedata = []
        logger.debug("get 요청 받음")

        logger.debug("mongo test")
        for cu in cursor:
            del cu['_id']
            responsedata.append(cu)

        return HttpResponse(json.dumps(responsedata), status=200)


# docker build -t colvet/djangotest .
# docker run -d -p 8083:8083 --name django -v /Users/colvet/Documents/data:/usr/src/app/data colvet/djangotest:latest
