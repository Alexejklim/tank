# PyTank
Robot for remote presence based on Raspberry Pi.

## Common info:

## Tips for installing:
1. Python version: *2.7.14*.
2. [Required moduls](../master/requirements.txt)
3. To run client on windows requiered also pygi-aio(3.24.1_rev1), gstreamer (1.0).


## Useful things:
1. Add server to autostart in RPi: nano /etc/rc.local

## TODOs:
1. Deployment automation.
2. Add reboot RPi and softreboot server from client.
3. Debug audio section. Truble with control and stream quality.
4. Don`t work "socket.gethostbyname('raspberrypi')" in main.py
5. Set video control panel below video stream.
6. Debug servo control. Sometimes servo control lags. Mb switch sepatate client servo thread to joystick thread. Also can change http timeout.
7. Transition to Python3.
8. Crossplatform client.
8. Obstacle analysis.

## Gallery
![leftside](../master/images/tank_leftside.jpg)
![rightside](../master/images/tank_rightside.jpg)
![client](../master/images/clientscreen.PNG)

