FROM tiangolo/uwsgi-nginx:python3.6

LABEL maintainer="Sebastian Ramirez <tiangolo@gmail.com>"

ENV DEBIAN_FRONTEND noninteractive
ARG DEBIAN_FRONTEND=noninteractive

# pip mirror
ADD pip.conf /root/.config/pip/

RUN pip install --upgrade pip
RUN apt-get update
# RUN apt-get -y install cifs-utils
RUN apt-get -y install doxygen
RUN apt-get install -y --no-install-recommends apt-utils
RUN apt-get install -y dialog
RUN apt-get -y install software-properties-common

# install openjdk-8
# RUN apt-get install -y openjdk-8-jdk
# RUN apt-get install -y openjdk-8-jre
# RUN update-alternatives --config java
# RUN update-alternatives --config javac

#RUN \
#  echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections && \
#  add-apt-repository -y ppa:webupd8team/java && \
#  apt-get update && \
#  apt-get install -y oracle-java8-installer && \
#  apt-get install oracle-java8-set-default && \
#  rm -rf /var/lib/apt/lists/* && \
#  rm -rf /var/cache/oracle-jdk8-installer


# URL under which static (not modified by Python) files will be requested
# They will be served by Nginx directly, without being handled by uWSGI
ENV STATIC_URL /static
# Absolute path in where the static files wil be
ENV STATIC_PATH /app/app/static
#ENV STATIC_PATH /root/data

# If STATIC_INDEX is 1, serve / with /static/index.html directly (or the static URL configured)
# ENV STATIC_INDEX 1
ENV STATIC_INDEX 0

# Add demo app
COPY . /app
WORKDIR /app
# RUN ls -la
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install psycopg2-binary

#RUN mkdir ~/data
#RUN chmod 777 ~/data
# RUN ln -s /app/static ~/data

# Make /app/* available to be imported by Python globally to better support several use cases like Alembic migrations.
ENV PYTHONPATH=/app

# Copy start.sh script that will check for a /app/prestart.sh script and run it before starting the app
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Move the base entrypoint to reuse it
RUN mv /entrypoint.sh /uwsgi-nginx-entrypoint.sh
# Copy the entrypoint that will generate Nginx additional configs
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Supervisor, which in turn will start Nginx and uWSGI
CMD ["/start.sh"]
# CMD mount.cifs //$RELEASE_FILE_SRV/data /app/static -o file_mode=0777,dir_mode=0777,rw,iocharset=utf8,\
#     username=$RELEASE_FILE_USER,password=$RELEASE_FILE_PASSWD; \
#     /start.sh
