FROM python:3
WORKDIR /usr/src/app

## Install packages
COPY requirements.txt ./
RUN pip install -r requirements.txt

## Copy all src files
COPY . .

## Run the application on the port 8080
EXPOSE 8083
CMD ["gunicorn", "--bind", "0.0.0.0:8083","djangoservice.wsgi:application"]


# docker run -d -p 8083:8083 --network test --name django colvet/django-app-service:latest