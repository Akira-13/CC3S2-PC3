#!/bin/bash

FILES=$(ls /tmp/*.txt)

echo $1

cat file.txt | grep "something"

echo `date`

cmd="ls -l"
eval $cmd

echo "Enter your name:"
read name
echo "Hello $name"
