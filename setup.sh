#!/bin/bash

# make symbolic link from serial port 0 to /dev/prolite
if [ -a /dev/prolite ];
then
    echo "/dev/prolite already exists."
else
    ln -s /dev/ttyS0 /dev/prolite
    chmod a+rw /dev/prolite
fi

# configure serial port settings (post CR+NL, no echo, 9600 baud)
stty opost -ocrnl onlcr -echo 9600 < /dev/prolite

# pre-load idle display onto sign
echo "<ID01><PJ><FU><SD>BZFlag        <FZ>W" > /dev/prolite
echo "Pre-loaded page J"
sleep 1
echo "<ID01><PW><FU>NOT CONNECTED TO SERVER.             <FZ>X" > /dev/prolite
echo "Pre-loaded page W"
sleep 1
echo "<ID01><PX><FN><FZ>J" > /dev/prolite
echo "Pre-loaded page X"
sleep 1
echo "<ID01><PI><FU><SD>BZFlag        <FZ>K" > /dev/prolite
echo "Pre-loaded page I"
sleep 1
echo "<ID01><RPJ>" > /dev/prolite

