#!/bin/bash

set -e

CSIRTG_USER=$CSIRTG_USER
CSIRTG_FEED=$CSIRTG_FEED
CSIRTF_TOKEN=$CSIRTG_TOKEN

docker pull csirtgadgets/honeypot-http

docker run \
  -p 80:8080 \
  -e CSIRTG_USER=${CSIRTG_USER} \
  -e CSIRTG_FEED=${CSIRTG_FEED} \
  -e CSIRTG_TOKEN=${CSIRTG_TOKEN} \
  -e TRACE=1 \
  csirtgadgets/honeypot-http
