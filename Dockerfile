FROM ubuntu:16.04

MAINTAINER Strelnikov Oleg

RUN apt-get -y update

# Установка postgresql

ENV PGVER 9.5

RUN apt-get install -y postgresql-$PGVER
RUN apt-get install postgresql-contrib-$PGVER
# Установка Python3
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install cython
RUN pip3 install pytz
RUN pip3 install python-dateutil
RUN pip3 install py-postgresql
RUN pip3 install gunicorn
RUN pip3 install --no-binary :all: falcon

USER postgres
RUN /etc/init.d/postgresql start &&\
    psql -c "CREATE DATABASE tech_db WITH template=template0 encoding='UTF8';" &&\
    psql --command "CREATE USER forum WITH PASSWORD 'forum';" &&\
    psql -c "grant all privileges on database tech_db to forum;" &&\
    psql -d "tech_db" -c "CREATE EXTENSION CITEXT;" &&\
    psql -c "SELECT * FROM pg_collation;" &&\
    /etc/init.d/postgresql stop

# Adjust PostgreSQL configuration so that remote connections to the
# database are possible.
RUN echo "host all  all    0.0.0.0/0  trust" >> /etc/postgresql/$PGVER/main/pg_hba.conf
RUN echo "local all all trust" >> /etc/postgresql/$PGVER/main/pg_hba.conf
RUN echo "host  all all 127.0.0.1/32 trust" >> /etc/postgresql/$PGVER/main/pg_hba.conf
RUN echo "host  all all ::1/128 trust" >> /etc/postgresql/$PGVER/main/pg_hba.conf

RUN echo "listen_addresses='*'" >> /etc/postgresql/$PGVER/main/postgresql.conf
RUN echo "synchronous_commit=off" >> /etc/postgresql/$PGVER/main/postgresql.conf

# Expose the PostgreSQL port
EXPOSE 5432

# Add VOLUMEs to allow backup of config, logs and databases
VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

# Back to the root user
USER root

# Копируем исходный код в Docker-контейнер
ENV WORK /opt/tech_db_forum
ADD tech_db_forum/ $WORK/tech_db_forum/
ADD table_create.sql $WORK/table_create.sql

# Объявлем порт сервера
EXPOSE 5000

#
# Запускаем PostgreSQL и сервер
#
RUN ls $WORK/tech_db_forum
ENV PGPASSWORD forum
CMD service postgresql start &&\
    cd $WORK/ &&\
    psql -h localhost -U forum -d tech_db -f table_create.sql &&\
gunicorn -w 8 -t 360 -b :5000 tech_db_forum.app