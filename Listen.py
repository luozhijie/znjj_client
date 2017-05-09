# coding:utf8
import urllib.request
import urllib
import json
import RPi.GPIO as GPIO
import time
import dht11

# 主机地址
host = "192.168.1.144:8080"
# 网址
url = "http://" + host + "/znjj/ListenService"
# post 参数
pdata = {'username': 'admin', 'password': 'admin'}
pdata = urllib.parse.urlencode(pdata)
binary_data = pdata.encode('utf-8')
# 循环次数，用来判断时间 几次后再发送温度数据
times = 28;
while True:
    times += 1
    f = urllib.request.urlopen(url, binary_data)
    data = f.read()
    data = data.decode('UTF-8')
    datas = json.loads(data)

    # print(data)
    GPIO.cleanup();
    GPIO.setmode(GPIO.BCM);
    for a in datas['deviceList']:
        print(a['deviceType']['deviceTypeId'])
        gpio = a['device_gpio'];
        # 设备类型为遥控器的动作
        if a['deviceType']['deviceTypeId'] == 1:
            print("遥控动作")
        # 设备类型为开关的动作
        if a['deviceType']['deviceTypeId'] == 2:

            # print(gpio)
            if a['deviceStat'] == '0':
                # print("off")
                # 关
                GPIO.cleanup(gpio);
            else:
                # 开
                # print("on")
                GPIO.setup(gpio, GPIO.OUT);
        # 设备类型为温度湿度传感器的动作
        if a['deviceType']['deviceTypeId'] == 3:
            if times == 30:
                print("提交温湿度")
                times = 0;
                # 读取dht11数据
                dht11 = dht11.DHT11(gpio)
                tempInfo = dht11.read();
                # 判断是否读取成功
                if tempInfo.is_valid():
                    # 温度
                    temperature = tempInfo.temperature;
                    # 湿度
                    humidity = tempInfo.humidity;
                    # 发送数据
                    # 网址
                    url2 = "http://" + host + "/znjj/SendInfoServlet?stat=temp"
                    # post 参数
                    pdata2 = {'temperature': temperature, 'humidity': humidity, 'deviceId': a['deviceId']}
                    pdata2 = urllib.parse.urlencode(pdata2)
                    binary_data2 = pdata2.encode('utf-8')
                    f = urllib.request.urlopen(url2, binary_data2)
                    data2 = f.read()
                    data2 = data2.decode('UTF-8')
                    if data2 == 'OK':
                        print("上传成功")

    time.sleep(5)
