# Build with (x.x.x means release version number):
# sudo docker build -t dockerhubContainer/bdms:x.x.x ./config 
# Test with:
# sudo docker run -it --rm --name bmsContainer -p 80:80 dockerhubContainer/bdms:x.x.x /bin/sh 
# Run with:
# sudo docker run -d --name bmsContainer -p 80:80 dockerhubContainer/bdms:x.x.x

FROM ubuntu

LABEL maintainer="davide.zanin@supsi.ch"

# Setting default args that become an env variable,
# you can passing it during build with --build-arg 
# ( e.g --build-arg SERVER_RELEASE=x.x.x)
# Setting Release, Time Zone and DB parameters
ARG FEND_RELEASE=1.0.0
ARG SERVER_RELEASE=1.0.0
ARG A_DB_USER='postgres'
ARG A_DB_PASS='postgres'
ARG A_DB_NAME='bms'
ARG A_TZ='Europe/Zurich'
# Gitlab repo
# ARG A_REPO_PATH='git@gitlab.com:davideZanin'
# ARG A_FEND_NAME_REPO='bms-webapp'
# ARG A_SERVER_NAME_REPO='server'
# Github fork
# ARG A_REPO_PATH='https://github.com/dzanin'
ARG A_REPO_PATH='https://github.com/geoadmin'
ARG A_FEND_NAME_REPO='bdms-web'
ARG A_SERVER_NAME_REPO='bdms-service'
ARG A_SITE='swisstopo.ch'

ENV FEND_RELEASE_VERSION=${FEND_RELEASE}
ENV SERVER_RELEASE_VERSION=${SERVER_RELEASE}
ENV REPO_PATH=${A_REPO_PATH}
ENV FEND_NAME_REPO=${A_FEND_NAME_REPO}
ENV SERVER_NAME_REPO=${A_SERVER_NAME_REPO}
ENV DB_USER=${A_DB_USER}
ENV DB_PASS=${A_DB_PASS}
ENV DB_NAME=${A_DB_NAME}
ENv SITE=${A_SITE}
ENV TZ=${A_TZ}

# Adjusting Timezone in the system
RUN echo $TZ > /etc/timezone && \
    apt-get update && apt-get install -y tzdata && \
    rm /etc/localtime && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get clean

# Install SSH, copy private/public key for gitlab, add gitlab to known_host
# RUN apt-get -y update &&\
#     apt-get -y install --no-install-recommends git ssh
# WORKDIR /root
# RUN mkdir -p /root/.ssh 
# COPY keys .ssh 
# RUN ssh-keyscan -H 'gitlab.com' >> ~/.ssh/known_hosts

# Switch to / directory
WORKDIR /

# Update, install python3.7, postgresql, nginx download release passed as arg and copy in /usr/src/app
RUN apt-get -y update &&\
    apt-get -y install unzip &&\
    apt-get -y install python3.7 &&\
    apt-get -y install python3-pip &&\
    apt-get -y install nginx &&\
    apt-get -y install nano &&\
    apt-get -y install npm &&\
    apt-get -y install git &&\
    DEBIAN_FRONTEND=noninteractive apt-get -y install postgresql postgresql-contrib &&\
    apt-get -y install postgis

# Clone from repository
RUN git clone ${REPO_PATH}/${FEND_NAME_REPO}.git 
RUN git clone ${REPO_PATH}/${SERVER_NAME_REPO}.git

# npm install and build
RUN cd ${FEND_NAME_REPO} &&\
    npm install &&\
    npm install axios &&\
    npm run build 

    # Use with github tag-version
    # apt-get -y install wget &&\
    # wget ${REPO_PATH}/${SERVER_NAME_REPO}/archive/${SERVER_RELEASE_VERSION}.tar.gz &&\
    # mv ${SERVER_RELEASE_VERSION}.tar.gz server.tar.gz &&\
    # wget ${REPO_PATH}/${FEND_NAME_REPO}/archive/${FEND_RELEASE_VERSION}.tar.gz &&\
    # mv ${FEND_RELEASE_VERSION}.tar.gz html.tar.gz &&\
    # tar xvzf server.tar.gz &&\
    # tar xvzf html.tar.gz &&\

# Create folders and move cloned file to /usr/src/swisstopo in html or server location
RUN cd .. &&\
    mkdir -p /usr/src/swisstopo/server &&\
    mkdir -p /usr/src/swisstopo/html
    # Use with github release-tag version
    # mv ${SERVER_NAME_REPO}-${SERVER_RELEASE_VERSION}/* /usr/src/swisstopo/server/  &&\
    # mv ${FEND_NAME_REPO}-${FEND_RELEASE_VERSION}/* /usr/src/swisstopo/html/ &&\

# Use with gitlab without builded frontend   
RUN mv ${SERVER_NAME_REPO}/* /usr/src/swisstopo/server/ 
RUN cd ${FEND_NAME_REPO} &&\
    mv build/* /usr/src/swisstopo/html/

# Switch to app directory
WORKDIR /usr/src/swisstopo/server

# Unzip sql
RUN cd db &&\
    unzip sql.zip

# Passing sql from host
# COPY bdms.sql /usr/src/swisstopo/server/config/

# Install requirements, add user/group docker
RUN python3.7 -m pip install -r requirements.txt &&\
    set -eux; 
    # \
	  # groupadd -r ${DB_USER} --gid=1001; \
	  # useradd -r -g ${DB_USER} --uid=1001 --no-create-home ${DB_USER}; 

# Run the rest of the commands as the ``postgres`` user 
USER postgres

# Add password "postgres" to user postgres, create db, add .sql
RUN /etc/init.d/postgresql start &&\
    psql --command "ALTER USER ${DB_USER} WITH PASSWORD '${DB_PASS}'; SET TIME ZONE '${TZ}';" &&\
    createdb -O ${DB_USER} ${DB_NAME} &&\
    psql -U postgres -d ${DB_NAME} -a -f db/1_schema.sql &&\
    psql -U postgres -d ${DB_NAME} -a -f db/2_data.sql &&\
    psql -U postgres -d ${DB_NAME} -a -f db/3_cantons.sql &&\
    psql -U postgres -d ${DB_NAME} -a -f db/4_municipalities.sql

# Create a PostgreSQL role named ``docker`` with ``docker`` as the password, 
# set the time zone, and then create a database `docker` owned by the ``docker
# ``role. 
# RUN /etc/init.d/postgresql start &&\
#     psql --command "CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASS}'; SET TIME ZONE '${TZ}';" &&\
#     createdb -O ${DB_USER} ${DB_NAME} &&\
#     psql -U postgres -d ${DB_NAME} -a -f db/1_schema.sql &&\
#     psql -U postgres -d ${DB_NAME} -a -f db/2_data.sql &&\
#     psql -U postgres -d ${DB_NAME} -a -f db/3_cantons.sql &&\
#     psql -U postgres -d ${DB_NAME} -a -f db/4_municipalities.sql
  #  DB useful commands
  #  psql -U postgres -d ${DB_NAME} -a -f db/bdms.sql
  #  PGPASSWORD=${DB_PASS} pg_restore -h localhost -p 5432 -U ${DB_USER} -d ${DB_NAME} -v "config/bdms.backup" -w
  #  pg_restore -U postgres -d ${DB_NAME} -a -f config/bdms.backup


# Add VOLUMEs to allow backup of config, logs and databases
VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]    

# Run the rest of the commands as the ``root`` user 
USER root

# Configure nginx: add proxy.conf, add an available site, create a like to enable site
RUN chmod +x config/my_wrapper_script.sh &&\
    rm /etc/nginx/sites-enabled/default &&\
#   chown -R $USER:$USER /var/www/example.com/html &&\
#   mv html/index.html /var/www/example.com/html/ &&\
    chown -R $USER:$USER /usr/src/swisstopo/html &&\
    mv config/${SITE} /etc/nginx/sites-available/ &&\
    mv config/proxy.conf /etc/nginx/proxy.conf &&\
    ln -s /etc/nginx/sites-available/${SITE} /etc/nginx/sites-enabled/

# Expose port 80
EXPOSE 80

# Run bash script
CMD ["./config/my_wrapper_script.sh"]
