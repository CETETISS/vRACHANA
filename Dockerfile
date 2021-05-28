FROM ubuntu:18.04

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

RUN apt-get install -y software-properties-common  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}
RUN apt-get install -y wget curl gnupg2 ca-certificates   | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}

RUN curl -sL https://deb.nodesource.com/setup_15.x | bash - \
   &&  apt-get install apt-transport-https -y  \
   &&  add-apt-repository -y ppa:nginx/stable  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}

RUN apt-get update  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}
RUN apt-get upgrade -y | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}

RUN apt-get install -y gettext  dialog net-tools build-essential git python3 python3-pip python3-setuptools python3-dev rcs emacs libjpeg-dev memcached libevent-dev libfreetype6-dev zlib1g-dev
RUN apt-get install -y nginx supervisor curl make     openssh-client openssh-server   libpq-dev    | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}
RUN apt-get install -y ffmpeg  ffmpeg2theora     bash-completion cron    nodejs     duplicity   libssl-dev libffi-dev   libxml2-dev libxslt1-dev python3-psycopg2 | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}
RUN DEBIAN_FRONTEND=noninteractive  apt-get install -y mailutils postfix | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}

RUN pip3 install pip==20.2.1
RUN pip3 install uwsgi nodeenv

#RUN npm i popper.js  \
RUN npm install -g @popperjs/core  \
   &&  npm install -g jquery@3.2.1  \
   &&  npm install -g bootstrap@4.3.1  \
   &&  npm install -g ekko-lightbox@5.3.0  \
   &&  npm install -g jquery-validation@1.19.1  \
   &&  npm install -g clipboard@2.0.4  \
   &&  npm install -g @fortawesome/fontawesome-free@5.8.2 | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}


RUN mkdir -p /home/docker/code/   \
   &&  mkdir -p /data/rcs-repo   \
   &&  mkdir -p /data/media   \
   &&  mkdir -p /data/heartbeats   \
   &&  echo "code, data, rcs-repo, media and heartbeats driectories are created"  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}

# change the working directory to "/home/docker/code"
WORKDIR "/home/docker/code/"

RUN apt-get update

# install clixoer docker code
RUN git clone -b v2 https://github.com/shivani2314/clixoer-docker.git  
RUN mv clixoer-docker/* . && rm -rf clixoer-docker

WORKDIR "/home/docker/code/"

RUN git clone -b stack-updation https://github.com/CLIxIndia-Dev/clixoer.git

# RUN pip install to install pip related required packages as per requirements.txt
RUN pip3 install -r /home/docker/code/clixoer/requirements.txt
RUN pip3 install cryptography --upgrade

# checking the present working directory and copying of configfiles : {copying the '.emacs' file in /root/ } , {copying the 'maintenance' files in /home/docker/code/clixoer/gnowsys-ndf/gnowsys_ndf/ndf/templates/ } , {copying wsgi file to appropriate location}, {copying postgresql conf file to appropriate location} , 
RUN pwd  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}    \
   &&  cp -v /home/docker/code/confs/emacs /root/.emacs  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}    \
   && cat /home/docker/code/confs/bash_compl >> /root/.bashrc   | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}

# setup all the configfiles (nginx, supervisord and postgresql)
RUN echo "daemon off;" >> /etc/nginx/nginx.conf   \
   &&  rm /etc/nginx/sites-enabled/default  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}   \
   &&  mv -v /etc/nginx/nginx.conf /tmp/  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}   \
   &&  ln -s /home/docker/code/confs/nginx.conf /etc/nginx/  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}   \
   &&  ln -s /home/docker/code/confs/nginx-app.conf /etc/nginx/sites-enabled/  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}   \
   &&  ln -s /home/docker/code/confs/supervisor-app.conf /etc/supervisor/conf.d/  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}   \
   &&  mv -v /etc/mailname /tmp/  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}   \
   &&  ln -s /home/docker/code/confs/mailname /etc/mailname  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}   \
   &&  mv -v /etc/postfix/main.cf /tmp/  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}   \
   &&  ln -s /home/docker/code/confs/main.cf /etc/postfix/  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}   \
   &&  ln -s /home/docker/code/confs/sasl_passwd /etc/postfix/  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}   \
   &&  ln -s /home/docker/code/confs/sasl_passwd.db /etc/postfix/  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}   

RUN groupadd -r mongodb   \
   &&  useradd -r -g mongodb mongodb  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}

RUN wget -qO - https://www.mongodb.org/static/pgp/server-3.6.asc | apt-key add -
RUN echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/3.6 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-3.6.list
RUN apt-get update  \
   &&  DEBIAN_FRONTEND=noninteractive apt-get install -y mongodb-org=3.6.21 mongodb-org-server=3.6.21 mongodb-org-shell=3.6.21 mongodb-org-mongos=3.6.21 mongodb-org-tools=3.6.21  \
   &&  rm -rf /var/lib/mongodb \
   &&  mv /etc/mongod.conf /etc/mongod.conf.orig  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}

RUN mkdir -p /data/db && chown -R mongodb:mongodb /data/db  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}
VOLUME /data

RUN echo "Size of deb packages files : "  du -hs  /var/cache/apt/archives/   \
   &&  ls -ltr  /var/cache/apt/archives/   \
   &&  du -hs  /var/cache/apt/archives/*   \
   &&  rm -rf /var/cache/apt/archives/*.deb

RUN echo "EXPOSE  22  25  443  80  8000  1025  143  587 9201"  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}
EXPOSE  22  25  443  80  8000  1025  143  587  27017  8080 5555 9201

RUN ln -sf /usr/share/zoneinfo/Asia/Kolkata /etc/localtime  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}
   #&&  pip install -U pyyaml nltk  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}   \
   #&&  /home/docker/code/scripts/nltk-initialization.py  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}

RUN django-admin.py compilemessages -l hi  \
   &&  django-admin.py compilemessages -l pu  \
   &&  django-admin.py compilemessages -l ta  \
   &&  django-admin.py compilemessages -l te  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /" 2>&1 | tee -a ${LOG_INSTALL_DOCKER}

RUN echo yes | /usr/bin/python /home/docker/code/clixoer/gnowsys-ndf/manage.py collectstatic

CMD /home/docker/code/scripts/initialize.sh  | sed -e "s/^/$(date +%Y%m%d-%H%M%S) :  /"  2>&1 | tee -a ${LOG_INSTALL_DOCKER}




