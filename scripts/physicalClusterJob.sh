#!/bin/bash/
while true
do
    cd /home/bronson/Projects/Group8/monitoring/ && venv/bin/flask scheduledlogging >>scheduled.log 2>&1
    sleep 5
done