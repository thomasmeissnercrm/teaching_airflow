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

### Install docker (https://docs.docker.com/install/linux/docker-ce/ubuntu/)
RUN curl -fsSL https://get.docker.com -o get-docker.sh \
 && sh get-docker.sh \
 && usermod -aG docker airflow

# Install kubectl (For cubernetes operator to work)
#	https://kubernetes.io/docs/tasks/tools/install-kubectl/
RUN apt-get update && sudo apt-get install -y apt-transport-https
RUN curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
RUN echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list.d/kubernetes.list
RUN apt-get update
RUN apt-get install -y kubectl && rm -rf /var/lib/apt/lists/* && apt-get clean

# Install Amazon’s authenticator for kubectl and IAM (for execution of kubectl command in Sumup dev-BI AWS environment)
#	https://docs.aws.amazon.com/eks/latest/userguide/install-aws-iam-authenticator.html
RUN curl -o aws-iam-authenticator https://amazon-eks.s3-us-west-2.amazonaws.com/1.12.7/2019-03-27/bin/linux/amd64/aws-iam-authenticator
RUN chmod +x ./aws-iam-authenticator
RUN mkdir -p $HOME/bin && cp ./aws-iam-authenticator $HOME/bin/aws-iam-authenticator && export PATH=$HOME/bin:$PATH
RUN cp ./aws-iam-authenticator /usr/bin/aws-iam-authenticator

USER airflow
WORKDIR /usr/local/airflow
ENTRYPOINT ["/entrypoint.sh"]
CMD ["webserver"]