# emulate-bluetooth-hid

## Install Bluetooth
This step is the same process as for Step 03 of the original article.

> sudo apt-get install -y python-gobject bluez bluez-tools python-bluez python-dev python-pip python-gtk2

> sudo pip2 install evdev

## Bluetooth Daemon Configuration
This is where things start to diverge. Bluez 5 uses a different mechanism than Bluez 4 to configure plug-ins and SDP profiles.  It is no longer possible to disable plug-ins using /etc/bluetooth/main.conf

Instead, I found that the easiest thing to do was to kill the bluetooth daemon and run it in the foreground

 - Stop the background process

> sudo /etc/init.d/bluetooth stop

 - Open a dedicated terminal and tun the bluetooth daemon in the foreground

> sudo /usr/sbin/bluetoothd --nodetach --debug -p time


Note: This will disable all bluetooth plug-ins except the time plug-in.  I found this the easiest way to ensure that plug-ins were not interfering with the keyboard emulator. An improvement would be to identify and disable only the plug-ins that would conflict with the emulator code.

## Configure DBUS
My reworked version of the keyboard emulator sets itself up as a DBUS system bus server.  This allows client applications to use DBUS to send keystrokes to the emulator and allows the simple creation of multiple different types of clients.

For this to work, the DBUS system bus needs to be configured to add the btkserver API.  This is enabled by copying a configuration file into the /etc/dbus-1/system.d folder

> sudo cp dbus/org.yaptb.btkbservice.conf /etc/dbus-1/system.d
