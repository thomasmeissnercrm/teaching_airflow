import os
import time
from pathlib import Path

path_docker_airflow = Path('docker/airflow')
path_docker_python = Path('docker/python')
print(path_docker_airflow)

print('Build dockerfile for python')
os.system(f'docker build {path_docker_python} -t teaching_python:3')
print('Build dockerfile for airflow')
os.system(f'docker build {path_docker_airflow} -t teaching_airflow:main')

print('Rise env')
os.system('docker-compose -f airflow.yaml up -d')
print('Pause for 10 - databases need to start.')
time.sleep(10)
print('Load example data')
os.system('docker run -it --rm --name my-running-script --network=teaching_airflow_default '
          '-v "$PWD":/usr/src/myapp -w /usr/src/myapp teaching_python:3 python data_loader.py')
