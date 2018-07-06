#!/usr/bin/env bash
nohup gunicorn -w 1 -b 0.0.0.0:16888 reco_server:app --timeout 1800  &