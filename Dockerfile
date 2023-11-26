FROM python:3.10-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /source

COPY requirements.txt /source/

RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . /source/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]