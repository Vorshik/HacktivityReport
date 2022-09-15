FROM python:bullseye

COPY . /HacktivityReport
WORKDIR /HacktivityReport

RUN pip3 install -r requirements.txt
RUN flask db upgrade

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "0", "app:app"]