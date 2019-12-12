#!/bin/sh
### BEGIN INIT INFO  
# Provides:          hidclient 
# Required-Start:    $remote_fs
# Required-Stop:     $remote_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start or stop the /dev/video0 
### END INIT INFO
# 1. Copy this file to /etc/init.d/
# 2. sudo update-rc.d hidclient.sh defaults/remove
# 3. sudo service hidclient.sh start/stop
case $1 in
    start)
        echo "starting  hidclient...."
		/etc/init.d/bluetooth stop
		/usr/sbin/bluetoothd -p time > /dev/null 2>&1 &
		/home/pi/emulate-bluetooth-hid/hidclient > /dev/null 2>&1 &
    ;;
    stop)
        echo "stoping hidclient...."
        killall hidclient
        killall bluetoothd
    ;;
    *)
        echo "Usage: $0 (start|stop)"
    ;;
