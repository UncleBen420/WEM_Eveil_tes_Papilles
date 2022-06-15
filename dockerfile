FROM python:3.8-slim-buster

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN python -m spacy download fr_core_news_sm
COPY Backend/ .
CMD [ "./Backend.py"]
