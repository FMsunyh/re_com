#!/usr/bin/env bash
echo "reboot server"

ps -aux|grep reco_server |grep -v grep|cut -c 9-15|xargs kill -9

source deactivate
source activate zjai_com

nohup gunicorn -w 1 -b 0.0.0.0:16888 reco_server:app --timeout 1800  &