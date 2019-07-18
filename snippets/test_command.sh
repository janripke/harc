##!/usr/bin/env bash

echo 'TEST COMMAND, LINE 1'

sleep 1

echo "SLEPT ONE, SLEEPING SOME MORE"

sleep 2

echo "HERE'S A FILE:"
ls -l *.sh

echo "\n\nOK, NOW FOR THE FINAL TEST, HERE'S AN ERROR"
>&2 cat /this_doesnt_exist

sleep 1

echo "EXITING 3"
exit 3
