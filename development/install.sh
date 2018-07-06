#!/usr/bin/env bash
echo "Install commdity recogntion server"

#python_env="commdity_recognition"
python_env="zjai_com"
yaml="environment.yaml"
# workspace : /home/syh/commdity_recognition/development
workspace=$(cd `dirname $0`; pwd)
download_path=${workspace}"/server/static/download"
log_path=${workspace}"/server/log"

echo ${python_env}
echo ${workspace}
echo ${download_path}

if [ ! -d ${download_path} ]; then
    mkdir -p ${download_path}
fi

if [ ! -d ${log_path} ]; then
    mkdir -p ${log_path}
fi

check_conda=`conda -V`
echo "$check_conda"

echo "check env..."
check_env=`conda info -e | grep ${python_env}`
if [ "$check_env" != "" ];then
    echo "$check_env"
    echo "${python_env} is existed, it will be removed."
    conda remove --name ${python_env} --all
fi

echo "Processing........."
echo "Create python env........."
conda env create -f ${yaml}


