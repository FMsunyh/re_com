#!/usr/bin/env bash
ps -aux|grep reco_server |grep -v grep|cut -c 9-15|xargs kill -9