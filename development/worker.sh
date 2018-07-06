#!/usr/bin/env bash
echo "start server"
source deactivate
source activate zjai_com

nohup gunicorn -w 1 -b 0.0.0.0:16888 reco_server:app --timeout 1800  &