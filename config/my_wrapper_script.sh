#!/bin/bash

# Start the first process
service nginx start -D
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start my_first_process: $status"
  exit $status
fi

# Start the second process
service postgresql start
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start my_second_process: $status"
  exit $status
fi

# Start the third process
python3.7 bms/main.py
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start my_third_process: $status"
  exit $status
fi

# Naive check runs checks once a minute to see if either of the processes exited.
# This illustrates part of the heavy lifting you need to do if you want to run
# more than one service in a container. The container exits with an error
# if it detects that either of the processes has exited.
# Otherwise it loops forever, waking up every 60 seconds

while sleep 10; do
  ps aux |grep nginx |grep -q -v grep
  PROCESS_1_STATUS=$?
  #echo nginx: $PROCESS_1_STATUS
  ps aux |grep postgresql |grep -q -v grep
  PROCESS_2_STATUS=$?
  #echo postgres: $PROCESS_2_STATUS
  ps aux |grep main |grep -q -v grep
  PROCESS_3_STATUS=$?
  #echo app.py: $PROCESS_3_STATUS


  # If the greps above find anything, they exit with 0 status
  # If they are not both 0, then something is wrong
  if [ $PROCESS_1_STATUS -ne 0 -o $PROCESS_2_STATUS -ne 0 -o $PROCESS_3_STATUS -ne 0 ]; then
    echo -e "One of the processes has already exited (1 means exited): \n -Nginx: $PROCESS_1_STATUS, \n -Postgresql: $PROCESS_2_STATUS, \n -Tornado: $PROCESS_3_STATUS "
    exit 1
  fi
done