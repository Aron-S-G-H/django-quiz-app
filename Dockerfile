FROM python:3.10

WORKDIR /source

COPY requirements.txt /source/

RUN pip install -U pip && pip install -r requirements.txt

EXPOSE 8000

COPY . /source/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]