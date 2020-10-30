FROM python:3.8
WORKDIR /usr/src/app
COPY . /usr/src/app/

RUN pip install -r thesportsdb/requirements.txt --use-feature=2020-resolver
EXPOSE  9001
#ENV HOST=0.0.0.0



CMD [ "python" , "api-ml.py"]