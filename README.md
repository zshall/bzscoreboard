bzscoreboard
============

[Zach Hall](http://sosguy.net/), 2013

Posts messages from `bzadmin` to a Pro-Lite TruColorXP LED message sign.

Setup
=====

* You'll need Linux, Python 2, and `bzadmin` to run `bzscoreboard`. Additionally, your computer will need an RS232 serial port or a USB to RS232 adapter. You'll also need a Pro Lite TrucolorXP LED sign.

* This program assumes that your sign is connected to your computer at `/dev/stty0`. `$ sudo ./setup.sh` will create the symlink and configure the serial port for communication with the TruColorXP. If you are using a different serial port, you can edit `setup.sh` or run the commands in it manually.

* Pages I, J, K, L, M, O, P, Q, R, W, X, and Y will be used on your sign. `setup.sh` will pre-load some pages into the sign, while others will be constructed at runtime.

Running the program
===================

* Once you have run `setup.sh` and you see the "NOT CONNECTED TO SERVER" message, you are ready to go. `$ python bzscoreboard.py callsign@hostname` will start the program. If you don't include the callsign@hostname argument, the `bzscoreboard.py` will connect to `localhost` as `scoreboard`.

Features
========

* Displays server hostname and port

* Displays join and leave messages

* Displays chat messages

* Displays kill messages

Known issues
============

* At the moment, I don't know how to get the actual team scores of a BZFlag game in `bzadmin`. To be a true scoreboard, `bzscoreboard` will need some way of keeping track of scores.

* I don't know the syntax for suicide messages yet, so I can't program in a pattern to listen for them.

* If many messages are sent at once, the sign is overloaded. I hope to fix this soon.