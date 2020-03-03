# Tomcatv2

## How to run the IMU code:

Navigate to the IMU folder
```
g++ XsensIMU.cpp XsensIMU.h imutest.cpp -o imu
```
```
./imu
```

Right now it just takes 200 measurements, writes them to telem.txt, and streams the data over UDP port 5007 on 127.0.0.1

## Troubleshooting

*If you are getting IMU read errors, make sure the IMU is on and all the pins are connected. It needs SCL,SDA,GND, 3.3V, and DRDY connected to header pin 15 (GPIO 48).

*If you get GPIO read errors, make sure GPIO pin 48 is exported. If folder /sys/class/gpio/gpio48 doesn't exist, the the pin is not exported, and you can export it with:
```
cat 48 > /sys/class/gpio/export
