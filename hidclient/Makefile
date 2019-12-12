CFLAGS := $(shell pkg-config --cflags dbus-1)
hidclient: hidclient.c
	gcc -g `pkg-config --cflags dbus-1 gio-2.0`  hidclient.c -lbluetooth `pkg-config --libs dbus-1 gio-2.0` -ludev -o hidclient

test: test.c
	gcc -g `pkg-config --cflags gio-2.0`  test.c  `pkg-config --libs gio-2.0`  -o test