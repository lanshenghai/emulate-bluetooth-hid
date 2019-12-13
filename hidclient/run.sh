sudo /etc/init.d/bluetooth stop
sudo killall bluetoothd
sudo /usr/sbin/bluetoothd --nodetach --debug -p time
