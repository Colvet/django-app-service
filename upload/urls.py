from django.urls import path

from upload.Api import uploadapi

urlpatterns = [
    path('upload/', uploadapi.upload_file, name='upload_api'),
    path('test/', uploadapi.test)

]
