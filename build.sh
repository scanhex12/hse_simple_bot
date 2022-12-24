#!/bin/bash

docker compose build --build-arg IAM_TOKEN="$IAM_TOKEN" --build-arg FOLDER_ID="$FOLDER_ID"

if [[ "$1" = "run" ]]; then
    docker compose up
fi

