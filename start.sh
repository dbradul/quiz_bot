#!/bin/bash

# export env vars
export $(cat .env | sed 's/#.*//g' | xargs)

# restart in infinite loop
while :
do
  echo "Starting quiz bot..."
  python src/main.py
  sleep 1
done