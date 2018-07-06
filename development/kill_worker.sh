#!/usr/bin/env bash
echo "kill server"
ps -aux|grep reco_server |grep -v grep|cut -c 9-15|xargs kill -9