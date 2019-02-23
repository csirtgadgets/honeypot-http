#!/bin/bash

set -e

VERSION="$1"

docker tag csirtgadgets/honeypot-http:latest csirtgadgets/honeypot-http:${VERSION}
docker push csirtgadgets/honeypot-http:latest
docker push csirtgadgets/honeypot-http:${VERSION}
