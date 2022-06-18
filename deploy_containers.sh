#!/bin/bash

docker build -t backend_eveil .

cd GUI
docker build -t gui_eveil .

cd ../DataBase
# mkdir DockerData
# mkdir DockerData/Data

docker-compose up -d
