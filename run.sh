#!/bin/bash
source /home/frank/site/env/bin/activate
gunicorn -b 127.0.0.1:5001 manage:app