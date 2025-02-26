#!/bin/bash

# Fungsi untuk mengecek ketersediaan port
wait_for_port() {
  local port=$1
  echo "Waiting for port $port to be available..."
  while ! nc -z localhost $port; do
    sleep 1
  done
  echo "Port $port is available!"
}

# Tunggu port sesuai browser
if [ "$1" == "firefox" ]; then
  wait_for_port 4444
elif [ "$1" == "chrome" ]; then
  wait_for_port 4445
elif [ "$1" == "edge" ]; then
  wait_for_port 4446
fi