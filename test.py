import RPi.GPIO as GPIO
import time

GPIO.cleanup();
GPIO.setmode(GPIO.BCM);
while True:
    GPIO.setup(18,GPIO.IN)
    if GPIO.input(18):
        time.sleep(0.01)
        # 二次过滤
        if GPIO.input(18):
            print("有人")
    else:
        print("没人")
    time.sleep(1)
