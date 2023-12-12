# создание образа на основе python
FROM python:3.9.13

# установка виртуальных переменных
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# создание рабочей директории
WORKDIR /usr/src/transferring_things/ad_things

# выполнение команды
RUN pip install --upgrade pip
# копирование и установка requirements
COPY ./requirements.txt /usr/src/
RUN pip install -r /usr/src/requirements.txt

# копирование всего проекта
COPY ./ad_things /usr/src/transferring_things/ad_things
#CMD ["python", "manage.py", "migrate"]
#EXPOSE 8000
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
