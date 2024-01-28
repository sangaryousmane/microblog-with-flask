FROM python:3.9

RUN mkdir /home/python

WORKDIR /home/python/

COPY requirements.txt .

# Install all the dependencies
RUN pip install -r requirements.txt

# COPY the application files
COPY ./templates/ ./templates/
COPY ./posts/ ./posts/
COPY ./errors/ ./errors/
COPY ./users/ ./users/
COPY ./main/ ./
COPY ./instance/ ./instance/
COPY ./models/ ./models/
COPY ./static/ ./static/
COPY ./main.py .

CMD["python", "main.py"]
