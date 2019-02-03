FROM python:3.7
 ENV PYTHONUNBUFFERED 1
 RUN pip install --upgrade pip
 RUN pip install django>=2.0 pipenv
 RUN django-admin.py startproject --template=https://github.com/arocks/edge/archive/master.zip --extension=py,md,html,env my_proj . 
 # set working directory to /app
 WORKDIR my_proj/
 RUN pipenv install --dev
 COPY . /my_proj/ 
 
 
