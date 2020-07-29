import os
import sys
import time
from pathlib import Path
import argparse
import venv


path_docker_airflow = Path('docker/airflow')
path_docker_python = Path('docker/python')

passer = argparse.ArgumentParser(description="Control Airflow local ENV")

passer.add_argument('--reload_data', action='store_true', help='Reload data in all databases')
passer.add_argument('--start', action='store_true', help='Start airflow docker containers')
passer.add_argument('--stop', action='store_true', help='Stop airflow docker containers')
passer.add_argument('--restart', action='store_true', help='Restart airflow docker containers')
passer.add_argument('--remove', action='store_true', help='Delete all docker images, containers')
passer.add_argument('--rebuild', action='store_true', help='Rebuild airflow env')
passer.add_argument('--add_vir_env', action='store_true', help='Add virtual env')
passer.add_argument('--rm_vir_env', action='store_true', help='Remove virtual env')

arguments = passer.parse_args()


def reload_data():
    print('Load example data')
    os.system('docker run -it --network=airflow_network '
              f'-v {Path.cwd()}:/usr/src/myapp -w /usr/src/myapp teaching_python:3 python data_loader.py')
    print('Data load done.')


def airflow_start():
    print('Starting Airflow local env.')
    os.system('docker-compose -f airflow.yaml up -d')


def airflow_stop():
    print('Stopping Airflow env.')
    os.system('docker-compose -f airflow.yaml down')


def airflow_restart():
    print('Restarting docker containers')
    os.system('docker container restart teaching_airflow_webserver_1 teaching_airflow_scheduler_1 teaching_airflow_worker_1')


def airflow_build():
    print('Build dockerfile for python')
    os.system(f'docker build {path_docker_python} -t teaching_python:3')
    print('Build dockerfile for airflow')
    os.system(f'docker build {path_docker_airflow} -t teaching_airflow:main')


def remove_airflow():
    print('Killing all containers')
    os.system('docker kill $(docker ps -q)')
    print('Remove all containers')
    os.system('docker rm $(docker ps -a -q)')
    print('Removing all docker images')
    os.system('docker rmi -f $(docker images -q)')
    remove_virtual_env()


def full_build():
    airflow_build()
    airflow_start()
    print('Waiting 60 seconds for databases to start')
    time.sleep(60)
    reload_data()
    add_virtual_env()


def rebuild():
    remove_airflow()
    full_build()


def add_virtual_env():
    print('Creating virtual env')
    venv.create(Path('airflow_env'), with_pip=True)
    os.system(f'. airflow_env/bin/activate && pip install -r {path_docker_airflow}/python_req.txt')
    os.system(f'. airflow_env/bin/activate && AIRFLOW_GPL_UNIDECODE=yes pip install apache-airflow[s3,async,kubernetes,slack,ssh,redis,postgres,hive,mysql,gcp]==1.10.1')


def remove_virtual_env():
    print('Remove virtual env')
    os.system('rm -d -r airflow_env')


if arguments.reload_data:
    reload_data()
if arguments.start:
    airflow_start()
if arguments.stop:
    airflow_stop()
if arguments.restart:
    airflow_restart()
if arguments.remove:
    remove_airflow()
if arguments.rebuild:
    rebuild()
if arguments.add_vir_env:
    add_virtual_env()
if arguments.rm_vir_env:
    remove_virtual_env()

if len(sys.argv) == 1:
    full_build()
