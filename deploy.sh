#!/bin/bash

# DATABASE LAUNCHING
cd DataBase
mkdir DockerData
mkdir DockerData/Data

docker-compose up -d
unzip Data.zip -d DockerData

./UploadDataToES.py --path DockerData/Data/entree.jl
./UploadDataToES.py --path DockerData/Data/plat.jl
./UploadDataToES.py --path DockerData/Data/dessert.jl

./UploadDataWineToES.py --path DockerData/Data/vin_blanc.jl
./UploadDataWineToES.py --path DockerData/Data/vin_rouges.jl

# BACKEND LAUNCHING
cd ../Backend
./Backend.py
