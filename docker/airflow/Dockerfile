FROM puckel/docker-airflow:1.10.1

USER root
WORKDIR /usr/local/airflow

COPY python_req.txt /airflow_requirements.txt
# Authentication
RUN apt-get update \
 && apt-get install -y python-dev \
 && pip install flask-bcrypt \
 && mkdir -p /usr/share/man/man1 && mkdir -p /usr/share/man/man7 \
 && apt-get install sudo -y \
 && usermod -aG sudo airflow \
 && echo 'airflow     ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers \
 && addgroup --gid 9998 ssh_group \
 && adduser airflow ssh_group \
 && adduser root ssh_group \
 && apt-get install -y curl \
 && apt-get install -y libpq-dev \
 && apt-get install -y python-psycopg2 \
 && apt-get install -yqq  libkrb5-dev libsasl2-dev gcc mc \
 && sudo apt-get install -y apt-transport-https \
 && pip uninstall -yq pyopenssl psycopg2 psycopg2-binary \
 && apt-get install -y --no-install-recommends postgresql-client \
 && pip install pyopenssl psycopg2-binary \
 && pip install apache-airflow[s3,async,kubernetes,slack,ssh,redis,postgres,hive,mysql,gcp]==1.10.1 \
 && pip install -r /airflow_requirements.txt

USER airflow
WORKDIR /usr/local/airflow
ENTRYPOINT ["/entrypoint.sh"]
CMD ["webserver"]