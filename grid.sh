#! /bin/bash

if command -v docker-compose >/dev/null 2>&1; then
    compose="docker-compose"
else
    compose="docker compose"
fi

function run() {
    case $1 in
    'run')
      ${compose} --file 'docker-compose.yml' --project-name 'selenium-grid-upload' up ${@:2} -d
    ;;
    'start')
      ${compose} --file 'docker-compose.yml' --project-name 'selenium-grid-upload' start
    ;;
    'restart')
      ${compose} --file 'docker-compose.yml' --project-name 'selenium-grid-upload' restart
    ;;
    'stop')
      ${compose} --file 'docker-compose.yml' --project-name 'selenium-grid-upload' stop
    ;;
    'down')
      ${compose} --file 'docker-compose.yml' --project-name 'selenium-grid-upload' down
      docker images | grep "selenium-grid-upload_fastapi" | awk '{print $1":"$2}' | xargs docker rmi
    ;;
    *)  echo 'You do not select in [run, start, restart, stop, down]'
    ;;
esac
}

run $@