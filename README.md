# WEM_Eveil_tes_Papilles

## Budry Nohan, Dominguez Pierre and Vuagniaux Rémy

## Goal

The goal of this project is to create an application which can help a user cooking. It is build has a frontend backend database kind of architectural style. The database is a Elastic Search.

## Deployement

To deploy the app. The user has just to run the script deploy_container.sh
This script build the docker image for the backend and frontend. It run also a docker-compose.yml to deploy the complete environment.

You must add the data to the database by running the script upload_data.sh. Be careful to have python3 and elastic search version 7.10.0 installed to run this script. you can also upload the file with your own method but be careful to use the right schemas for the data.

## Access
There is the port which are exposed by the environnement.

- elasticsearch 9200 9300
- kibana 5601
- backend 8080
- frontend 3000
