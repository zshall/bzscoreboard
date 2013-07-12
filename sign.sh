#!/bin/bash

# This program simply echoes messages to the sign.
if [ -a /dev/prolite ];
then
    echo "$1" > /dev/prolite
fi
