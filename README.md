# pytank
Robot for remote presence based on Raspberry Pi.



## Useful info:
1. Add server to autostart in RPi: nano /etc/rc.local

## TODOs:
1. Deployment automation.
2. Add reboot RPi and softreboot server from client.
3. Debug audio section. Truble with control and stream quality.
4. Don`t work "socket.gethostbyname('raspberrypi')" in main.py
5. Set video control panel below video stream.
6. Debug servo control. Sometimes servo control has lags. Mb switch sepatate client servo thread to joystick thread. Also can change http timeout.
7. Obstacle analysis.

## Gallery
![leftside](../master/images/tank_leftside.jpg)
![rightside](../master/images/tank_rightside.jpg)
![client](../master/images/clientscreen.PNG)

