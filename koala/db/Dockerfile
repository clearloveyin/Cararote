############################################################
# Dockerfile to build iDesign container images
# Based on Ubuntu
############################################################
# Set the base image to Ubuntu
FROM ubuntu:16.04


############################################################
# install postgresql 9.5
RUN apt-get update && apt-get install -y wget
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN apt-get update
RUN apt-get -y install postgresql-9.5

USER postgres
RUN /etc/init.d/postgresql start \
    && psql --command "CREATE USER pger WITH SUPERUSER PASSWORD 'pger';" \
#    && psql --command "alter user postgres with password 'pset123456';" \
    && createdb -O pger pgerdb;
    

USER root
RUN echo "host	all	all	192.168.0.0/16	md5" >> /etc/postgresql/9.5/main/pg_hba.conf
RUN echo "listen_addresses='*'" >> /etc/postgresql/9.5/main/postgresql.conf

EXPOSE 5432

RUN mkdir -p /var/run/postgresql && chown -R postgres /var/run/postgresql
VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

USER postgres
CMD ["/usr/lib/postgresql/9.5/bin/postgres", "-D", "/var/lib/postgresql/9.5/main", "-c", "config_file=/etc/postgresql/9.5/main/postgresql.conf"]

