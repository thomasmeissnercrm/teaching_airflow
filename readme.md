# Teaching Airflow  
This repository contains a example environment that can be used
by anyone who wants how to code pipelines in Airflow

### Requirements

* Python 3.6 or higher https://www.python.org/
* Docker https://docs.docker.com/get-docker/
* Docker Compose https://docs.docker.com/compose/install/
* MySql client (ubuntu: ``sudo apt-get install libmysqlclient-dev``, mac: ```brew install mysql```)
* ONlY on Mac - Developer tools  ```xcode-select --install``` 

### Using repository
To start using repository just go in your terminal to folder when project was
cloned and type <br/> ```python3 teach_aiflow.py```  
What gonna happen:  
* Docker will build all needed images
* By Docker Compose a local cluster will be raised
* Example data wil be loaded into databases
* Virtual environment will be created
* All dependencies needed for Airflow will be installed inside virtual environment 

**Pre check**  
If for command ```docker ps``` you get error that cannot connect to docker engine
please try to run it with ```sudo```. If that work all commands here should be run with sudo as well.
### Additional commands
all should be run as ```python3 teach_airflow.py <argument>```
```
  --reload_data  Reload data in all databases
  --start        Start airflow docker containers
  --stop         Stop airflow docker containers
  --restart      Restart airflow docker containers
  --remove       Delete all docker images, containers
  --rebuild      Rebuild airflow env
  --add_vir_env  Add virtual env
  --rm_vir_env   Remove virtual env
```


### Connecting to extra services from PC level

#### Postgres
    * login: airflow
    * password: airflow
    * database: airflow
    * host: localhost
    * port: 5433

#### MySql
    * login: airflow
    * password: airflow
    * database: public
    * host: localhost
    * port: 3307

#### SFTP
    * username: airflow
    * password: airflow
    * port: 21
    