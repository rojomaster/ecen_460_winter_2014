raspivid -t 0 -w 800 -h 600 -fps 25 -hf -vf -b 1000000 -o - | gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay config-interval=1 pt=96 ! gdppay ! tcpserversink host=192.168.42.1 port=5000
