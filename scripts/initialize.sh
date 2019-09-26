#!/bin/bash

#Starting mongodb   
echo "No idea about arch hence starting normally.";
echo "[run] start mongod";
mongod  --config /home/docker/code/confs/mongod.conf & 

#sleep 60;

echo "[run] start postgresql" ;     # Used for postgres db
/etc/init.d/postgresql start ;      # Used for postgres db
#/etc/init.d/postgresql status ;      # Used for postgres db

echo "[run] start postfix" ;
/etc/init.d/postfix start ;

echo "[run] start ssh" ;
/etc/init.d/ssh start ;

echo "[run] start memcache" ;
/etc/init.d/memcached start

echo "[run] start rabbitmq-server" ;
/etc/init.d/rabbitmq-server start 

echo "[run]start elasticsearch" ;
/etc/init.d/elasticsearch start

echo "[run] go to the code folder" ;
cd /home/docker/code/clixoer/gnowsys-ndf/ ; 

echo "[run] smtpd.sh" ;
bash /home/docker/code/scripts/smtpd.sh ;

# nginx-app logs
if [[ -f /var/log/nginx/school.server.org.error.log ]] && [[ -f /var/log/nginx/school.server.org.access.log ]] ; then
    # files present in new location (/data/nginx-logs/) copy files appending ".old" to the filenames 
    if [[ -f /data/nginx-logs/school.server.org.error.log ]] && [[ -f /data/nginx-logs/school.server.org.access.log ]] ; then
        echo -e "\nWarning: (nginx-app logs) - Files found on both the locations. Please check nginx-app.conf for the logs paths." ;
        mv -v /var/log/nginx/school.server.org.error.log* /data/nginx-logs/school.server.org.error.log.old
        mv -v /var/log/nginx/school.server.org.access.log* /data/nginx-logs/school.server.org.access.log.old
    # files absent in new location (/data/nginx-logs/) copy files with the exact filenames
    elif [[ ! -f /data/nginx-logs/school.server.org.error.log ]] && [[ ! -f /data/nginx-logs/school.server.org.access.log ]] ; then
        echo -e "\nInfo: (nginx-app logs) - File found in old location and hence moving it to new location." ;
        if [[ -d /data/nginx-logs ]]; then
            echo -e "\nInfo: (nginx-app logs) - Directory already exists" ;    
        elif [[ ! -d /data/nginx-logs ]]; then
            echo -e "\nInfo: (nginx-app logs) - Directory doesn't exists. Hence creating it." ;
            mkdir -p /data/nginx-logs ;
        fi
        mv -v /var/log/nginx/school.server.org.error.log* /data/nginx-logs/
        mv -v /var/log/nginx/school.server.org.access.log* /data/nginx-logs/
    else
        echo -e "\nError: (nginx-app logs) - Oops something went wrong (/data/nginx-logs/*.logs). Contact system administator or CLIx technical team - Mumbai." ;
    fi
elif [[ ! -f /var/log/nginx/school.server.org.error.log ]] && [[ ! -f /var/log/nginx/school.server.org.access.log ]] ; then
    echo -e "\nInfo: (nginx-app logs) - Files doesn't exists. No action taken." ;
else
    echo -e "\nError: (nginx-app logs) - Oops something went wrong (/var/log/nginx/*.logs). Contact system administator or CLIx technical team - Mumbai." ;
fi

# nginx logs
if [[ -f /var/log/nginx/error.log ]] && [[ -f /var/log/nginx/access.log ]] ; then
    # files present in new location (/data/nginx-logs/) copy files appending ".old" to the filenames 
    if [[ -f /data/nginx-logs/error.log ]] && [[ -f /data/nginx-logs/access.log ]] ; then
        echo -e "\nWarning: (nginx logs) - Files found on both the locations(error.log and access.log). Please check nginx-app.conf for the logs paths." ;
        mv -v /var/log/nginx/error.log* /data/nginx-logs/error.log.old
        mv -v /var/log/nginx/access.log* /data/nginx-logs/access.log.old
    # files absent in new location (/data/nginx-logs/) copy files with the exact filenames
    elif [[ ! -f /data/nginx-logs/error.log ]] && [[ ! -f /data/nginx-logs/access.log ]] ; then
        echo -e "\nInfo: (nginx logs) - File found in old location and hence moving it to new location." ;
        if [[ -d /data/nginx-logs ]]; then
            echo -e "\nInfo: (nginx logs) - Directory already exists" ;    
        elif [[ ! -d /data/nginx-logs ]]; then
            echo -e "\nInfo: (nginx logs) - Directory doesn't exists. Hence creating it." ;
            mkdir -p /data/nginx-logs ;
        fi
        mv -v /var/log/nginx/error.log* /data/nginx-logs/
        mv -v /var/log/nginx/access.log* /data/nginx-logs/
    else
        echo -e "\nError: (nginx logs) - Oops something went wrong (/data/nginx-logs/*.logs). Contact system administator or CLIx technical team - Mumbai." ;
    fi
elif [[ ! -f /var/log/nginx/error.log ]] && [[ ! -f /var/log/nginx/access.log ]] ; then
    echo -e "\nInfo: (nginx logs) - Files doesn't exists. No action taken." ;
else
    echo -e "\nError: (nginx logs) - Oops something went wrong (/var/log/nginx/*.logs). Contact system administator or CLIx technical team - Mumbai." ;
fi

echo "[run] supervisord" ;
supervisord -n ;
