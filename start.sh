#!/bin/sh

export SLACKTOKEN=changem
export AWS_SECRET_ACCESS_KEY=changeme
export AWS_ACCESS_KEY_ID=changeme

exec python3 ./botex.py
