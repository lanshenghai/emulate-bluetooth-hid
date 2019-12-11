CFLAGS := $(shell pkg-config --cflags dbus-1)
hidclient: hidclient.c
	gcc -g `pkg-config --cflags dbus-1`  hidclient.c -lbluetooth `pkg-config --libs dbus-1` -o hidclient
