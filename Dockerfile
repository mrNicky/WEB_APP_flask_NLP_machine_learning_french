from python:3
 
RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /

CMD [ "python3", "main.py" ]
