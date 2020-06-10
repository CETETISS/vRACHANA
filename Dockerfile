FROM ubuntu:14.04

MAINTAINER shivani.dixit@tiss.edu

RUN useradd -ms /bin/bash docker

RUN su docker

RUN export DATE_LOG=`echo $(date "+%Y%m%d-%H%M%S")`
ENV LOG_DIR_DOCKER="/root/DockerLogs"   
ENV LOG_INSTALL_DOCKER="/root/DockerLogs/$(DATE_LOG)-gsd-install.log"

RUN echo "PATH="$LOG_DIR_DOCKER   \
   &&  mkdir -p $LOG_DIR_DOCKER   \
   &&  touch ${LOG_INSTALL_DOCKER}   \
   &&  ls ${LOG_INSTALL_DOCKER}   \
   &&  echo "Logs driectory and file created"  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}

RUN apt-get update  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}
RUN apt-get upgrade

RUN apt-get install -y wget

RUN apt-get install -y python-software-properties  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}   \
   &&  apt-get install -y software-properties-common python-software-properties  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}   \
   &&  add-apt-repository -y ppa:nginx/stable  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}   \
   &&  add-apt-repository -y ppa:mc3man/trusty-media  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}   \
   &&  apt-get install -y curl   \
   &&  curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -   \
   &&  curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -   \
   &&  echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list   \
   &&  add-apt-repository ppa:openjdk-r/ppa  \
   &&  wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -  \
   &&  apt-add-repository ppa:brightbox/ruby-ng  \
   &&  apt-get install apt-transport-https - --force-yes

RUN echo "deb https://artifacts.elastic.co/packages/6.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-6.x.list

RUN apt-key update && apt-get update  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}
RUN apt-get upgrade -y
RUN apt-get install -y openjdk-8-jdk

ENV JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64/

RUN apt-get install -y elasticsearch

RUN apt-get install -y dialog net-tools build-essential git python python-pip python-setuptools python-dev rcs emacs24 libjpeg-dev memcached libevent-dev libfreetype6-dev zlib1g-dev nginx supervisor curl g++ make     openssh-client openssh-server     mailutils postfix     sqlite3   libpq-dev postgresql-9.3 postgresql-contrib-9.3 python-psycopg2    ffmpeg gstreamer0.10-ffmpeg ffmpeg2theora     bash-completion cron     ruby2.4 ruby2.4-dev     nodejs     wget     duplicity   rabbitmq-server   yarn   libssl-dev libffi-dev   libxml2-dev libxslt1-dev | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}


RUN easy_install pip==9.0.1  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}

# install uwsgi now because it takes a little while
RUN pip install uwsgi nodeenv  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}

# for editing SCSS/SAAS stylesheets {compass}
RUN gem install compass  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}

RUN npm install -g popper.js@1.14.7  \
   &&  npm install -g jquery@3.2.1  \
   &&  npm install -g bootstrap@4.3.1  \
   &&  npm install -g ekko-lightbox@5.3.0  \
   &&  npm install -g highlight.js@9.15.6  \
   &&  npm install -g jquery-validation@1.19.1  \
   &&  npm install -g clipboard@2.0.4  \
   &&  npm install -g @fortawesome/fontawesome-free@5.8.2 | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}


# create code directory as it can't find dirctory while coping
RUN mkdir -p /home/docker/code/   \
   #&&  mkdir -p /data/db   \
   #&&  mkdir -p /data/rcs-repo   \
   #&&  mkdir -p /data/media   \
   &&  mkdir -p /data/heartbeats   \
   &&  echo "code, data, rcs-repo, media and heartbeats driectories are created"  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}

# change the working directory to "/home/docker/code"
WORKDIR "/home/docker/code/"

RUN apt-get update

# install clixoer docker code
RUN git clone https://github.com/shivani2314/clixoer-docker.git  
RUN mv clixoer-docker/* . && rm -rf clixoer-docker

#install clixoer code
RUN git clone https://github.com/CLIxIndia-Dev/clixoer.git

WORKDIR "/home/docker/code/"

# RUN pip install to install pip related required packages as per requirements.txt
RUN pip install -r /home/docker/code/clixoer/requirements.txt

# checking the present working directory and copying of configfiles : {copying the '.emacs' file in /root/ } , {copying the 'maintenance' files in /home/docker/code/clixoer/gnowsys-ndf/gnowsys_ndf/ndf/templates/ } , {copying wsgi file to appropriate location}, {copying postgresql conf file to appropriate location} , 
RUN pwd  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}    \
   &&  cp -v /home/docker/code/confs/emacs /root/.emacs  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}    \
   &&  rm /etc/postgresql/9.3/main/postgresql.conf  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}    \
   && cat /home/docker/code/confs/bash_compl >> /root/.bashrc   | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}

# setup all the configfiles (nginx, supervisord and postgresql)
RUN echo "daemon off;" >> /etc/nginx/nginx.conf   \
   &&  rm /etc/nginx/sites-enabled/default  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}   \
   &&  mv -v /etc/nginx/nginx.conf /tmp/  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}   \
   &&  ln -s /home/docker/code/confs/nginx.conf /etc/nginx/  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}   \
   &&  ln -s /home/docker/code/confs/nginx-app.conf /etc/nginx/sites-enabled/  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}   \
   &&  ln -s /home/docker/code/confs/supervisor-app.conf /etc/supervisor/conf.d/  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}   \
   &&  ln -s /home/docker/code/confs/postgresql.conf /etc/postgresql/9.3/main/  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}    \
   &&  mv -v /etc/mailname /tmp/  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}   \
   &&  ln -s /home/docker/code/confs/mailname /etc/mailname  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}   \
   &&  mv -v /etc/postfix/main.cf /tmp/  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}   \
   &&  ln -s /home/docker/code/confs/main.cf /etc/postfix/  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}   \
   &&  ln -s /home/docker/code/confs/sasl_passwd /etc/postfix/  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}   \
   &&  ln -s /home/docker/code/confs/sasl_passwd.db /etc/postfix/  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}   

RUN echo "Size of deb packages files : "  du -hs  /var/cache/apt/archives/   \
   &&  ls -ltr  /var/cache/apt/archives/   \
   &&  du -hs  /var/cache/apt/archives/*   \
   &&  rm -rf /var/cache/apt/archives/*.deb

RUN groupadd -r mongodb   \
   &&  useradd -r -g mongodb mongodb  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}
    
RUN echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.2 multiverse" > /etc/apt/sources.list.d/mongodb-org-3.2.list  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}

RUN apt-get update \
        && apt-get install -y --force-yes\
                mongodb-org=3.2.4 \
                mongodb-org-server=3.2.4 \
                mongodb-org-shell=3.2.4 \
                mongodb-org-mongos=3.2.4 \
                mongodb-org-tools=3.2.4 \
        && rm -rf /var/lib/mongodb \
        && mv /etc/mongod.conf /etc/mongod.conf.orig  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}

RUN rm -rf /data/db /data/media /data/rcs-repo

RUN cd /data/   \
   &&   wget http://clixplatform.tiss.edu/softwares/initial-schema-dump-clixplatform/clean-data-kedar-mrunal-20170324-clixplatform.tar.bz2   \
   &&   tar -xvjf clean-data-kedar-mrunal-20170324-clixplatform.tar.bz2

RUN rm -rf /data/rcs-repo/*  \
   && rm -rf /data/db/*

RUN mkdir -p /data/db && chown -R mongodb:mongodb /data/db  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}
VOLUME /data 

RUN echo "EXPOSE  22  25  443  80  8000  1025  143  587 9201"  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}
EXPOSE  22  25  443  80  8000  1025  143  587  27017  8080 5555 9201

RUN ln -sf /usr/share/zoneinfo/Asia/Kolkata /etc/localtime  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}  \
   &&  pip install -U pyyaml nltk  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}   \
   &&  /home/docker/code/scripts/nltk-initialization.py  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}

#RUN /etc/init.d/postgresql start  \
RUN service postgresql start  \
   &&  echo "psql -f /data/pgdata.sql;" | sudo su - postgres

RUN cd /home/docker/code/clixoer/gnowsys-ndf/   \
   &&  pip install flower==0.9.1  \
   &&  pip install Fabric==1.12.0  \
   &&  pip install requests==2.22.0

RUN echo yes | /usr/bin/python /home/docker/code/clixoer/gnowsys-ndf/manage.py collectstatic

CMD /home/docker/code/scripts/initialize.sh  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /"  2>&1 | tee -a ${LOG_INSTALL_DOCKER}




