#!/bin/bash
homepath=/home/iauto
source $homepath/py37env/bin/activate
export PYTHONPATH=$homepath/Spec2DB/koala/koala_server
rm -rf cache_root/*
lsof -i:25000 | grep python | awk '{print$2}' | xargs kill -9
python start.py
