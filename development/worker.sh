#!/usr/bin/env bash
nohup gunicorn -w 4 -b 0.0.0.0:11127 retrieval_server:app --timeout 1800  &