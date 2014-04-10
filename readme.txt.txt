These files are used for controlling a multicopter using a Raspberry Pi. A laptop running Linux connects to the Raspberry Pi wirelessly and can be used to send USB gamepad commands to the Raspberry Pi, which in turn are sent to the multicopter. Setup is as follows:

1) Establish wireless connection between Raspberry Pi and laptop
2) Connect gamepad to the laptop
3) Run server.py on the laptop, type in local IP address of laptop and port as follows: 192.168.xxx.xxx:8000
4) Run client.py on the Raspberry Pi, type in laptop IP address and port as follows: 192.168.xxx.xxx:8000 - now the Raspberry Pi will receive commands from the gamepad and send them to the flightboard via the Maestro board.
5) Ensure the PiCam is connected to the Raspberry Pi and configured properly to work
5) Run gstreamer.sh on the Raspberry Pi
6) Run gstreamer.sh on the Laptop - now a video feed should be visible on the laptop from the Raspberry Pi camera.