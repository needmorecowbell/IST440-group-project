#!/bin/sh

message=$1
maxKey=$2

for key in $(seq 1 $maxKey); do
    echo $key $message | tr $(printf %${key}s | tr ' ' '.')\A-Z A-ZA-Z
done