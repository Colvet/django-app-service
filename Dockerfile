FROM python:3
WORKDIR /usr/src/app

## Install packages
COPY requirements.txt ./
RUN pip install -r requirements.txt

## Copy all src files
COPY . .

## Run the application on the port 8080
EXPOSE 8083
CMD ["gunicorn", "--bind", "0.0.0.0:8083", "djangotest.wsgi:application"]


# docker run -d -p 8083:8083 -v /Users/colvet/Documents/data:/data --network test --name django-app-service colvet/djangotest:latest