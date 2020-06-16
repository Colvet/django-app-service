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
    for cu in cursor:
        del cu['_id']
        responsedata.append(cu)

    return HttpResponse(json.dumps(responsedata), status=200)


@csrf_exempt
def upload_file(request):
    print("????????????????????????????????????????")
    if request.method == 'POST':
        uploadFile = request.FILES['files']
        if uploadFile.name.find('csv') < 0:
            message = "파일형식이 잘못되었습니다"
            return HttpResponse(status=500)

        else:
            csv_file = pd.read_csv(uploadFile, encoding='utf8')
            df = pd.DataFrame(csv_file)
            time_now = datetime.now().timestamp()
            userName = request.POST['userName']

            # 디렉토리 저장 주소 설
            if not (os.path.isdir('data/' + userName)):
                print('디렉톨 ㅣ없다 !@#!@#@!#!@#!@#!@#!@#!@')
                os.makedirs(os.path.join('data/', userName))

            save_dir = 'data/' + userName

            # null 세고 지우기
            del_null_df, info = ms.analy(df)
            del_null_df.to_csv(os.path.join(save_dir, str(time_now) + "_" + uploadFile.name))

            FileSummaryData = {
                "originalLocation": os.path.join("save_dir", str(time_now) + "_" + uploadFile.name),
                "fileName": str(time_now) + "_" + uploadFile.name,
                "userName": userName,
                "info": info
            }
            return HttpResponse(status=200)
            collection.insert_one(FileSummaryData)

        return HttpResponse(status=200)

# docker build -t colvet/djangotest .
# docker run -d -p 8083:8083 --name django -v /Users/colvet/Documents/data:/usr/src/app/data colvet/djangotest:latest
