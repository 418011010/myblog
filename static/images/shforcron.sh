#!/bin/bash
    export PATH=$PATH:/usr/local/bin
    source /root/anaconda3/bin/activate py37
    cd ~/myblog/static/images/
    python ~/myblog/static/images/wordsrank.py
