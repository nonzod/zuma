# Webcam streaming

```
modprobe v4l2loopback
```

## Stream di un video su device v4l2loopback

```
ffmpeg -re -i /media/1000R/Video/VID_20130102_210749.mp4 -f v4l2 /dev/video0
```

Scalato:

```
ffmpeg -re -i /media/1000R/Video/VID_20130102_210749.mp4 -vf scale=640:360 -f v4l2 /dev/video0
```

## Stream da una IP CAM o IPWebcam Android su device v4l2loopback

```
ffmpeg -re -c mjpeg -i http://192.168.10.76:8080/video -pix_fmt yuv420p -vf scale=640:360 -f v4l2 /dev/video0
```
