#!/bin/bash

PORT=$1
if [ -z "$PORT" ]; then
  PORT=4444  # Default port jika tidak ada parameter
fi

until $(curl --output /dev/null --silent --head --fail http://localhost:$PORT); do
    echo "waiting for selenium hub on port $PORT to start"
    sleep 1
done