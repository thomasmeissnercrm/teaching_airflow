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
print('Pause for 60 - databases need to start.')
time.sleep(60)
print('Load example data')
os.system('docker run -it --network=airflow_network '
          f'-v {Path.cwd()}:/usr/src/myapp -w /usr/src/myapp teaching_python:3 python data_loader.py')
