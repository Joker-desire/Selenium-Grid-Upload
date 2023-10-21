#! /bin/bash

docker-compose -f docker-compose.yml up --scale chrome=1 --scale edge=1 --scale firefox=1 -d