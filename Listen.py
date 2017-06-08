# coding:utf8
import urllib.request
import urllib
import json
import RPi.GPIO as GPIO
import time
import dht11

# 主机地址
host = "192.168.43.143:8080"
# 网址
url = "http://" + host + "/znjjPage/ListenService"
# post 参数
pdata = {'username': 'admin', 'password': 'admin'}
pdata = urllib.parse.urlencode(pdata)
binary_data = pdata.encode('utf-8')
# 循环次数，用来判断时间 几次后再发送温度数据
times = 0
#  标记，用来判断是否是同一次可燃气体检测
flag1 = 0
# 标记， 用来判断是不是同一次人体检测
flag2 = 0
GPIO.setmode(GPIO.BCM);
GPIO.cleanup();
while True:
    times += 1
    f = urllib.request.urlopen(url, binary_data)
    data = f.read()
    data = data.decode('UTF-8')
    datas = json.loads(data)

    # print(data)
    for a in datas['deviceList']:
        print(a['deviceType']['deviceTypeId'])
        print(a['deviceStat'])
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
        if a['deviceType']['deviceTypeId'] == 3 and a['deviceStat'] == '1':
            print('temp')

            if times == 30:
                print("提交温湿度")
                times = 0;
                # 读取dht11数据
                dht11Info = dht11.DHT11(gpio)
                tempInfo = dht11Info.read();
                # 判断是否读取成功
                if tempInfo.is_valid():
                    # 温度
                    temperature = tempInfo.temperature;
                    # 湿度
                    humidity = tempInfo.humidity;
                    # 发送数据
                    # 网址
                    url2 = "http://" + host + "/znjjPage/SendInfoServlet?stat=temp"
                    # post 参数
                    pdata2 = {'temperature': temperature, 'humidity': humidity, 'deviceId': a['deviceId']}
                    pdata2 = urllib.parse.urlencode(pdata2)
                    binary_data2 = pdata2.encode('utf-8')
                    f = urllib.request.urlopen(url2, binary_data2)
                    data2 = f.read()
                    data2 = data2.decode('UTF-8')
                    if data2 == 'OK':
                        print("上传成功")
        # 设备类型为可燃气体检测的动作
        if a['deviceType']['deviceTypeId'] == 4 and a['deviceStat'] == '1':
            print("可燃气体检测")
            GPIO.setup(gpio, GPIO.IN);
            if GPIO.input(gpio):
                time.sleep(0.01)
                # 二次过滤
                if GPIO.input(gpio):
                    flag1 += 1;
                    if flag1 < 2:
                        # 网址
                        url2 = "http://" + host + "znjjPage//SendInfoServlet?stat=gas"
                        # post 参数
                        pdata2 = {'deviceId': a['deviceId']}
                        pdata2 = urllib.parse.urlencode(pdata2)
                        binary_data2 = pdata2.encode('utf-8')
                        f = urllib.request.urlopen(url2, binary_data2)
                        data2 = f.read()
                        data2 = data2.decode('UTF-8')
                        if data2 == 'OK':
                            print("上传成功")
                        else:
                            print("上传失败")
                        print('Input was HIGH')
            else:
                flag1 = 0
                print("save")
        # 设备类型为红外传感器 动作
        if a['deviceType']['deviceTypeId'] == 5:
            print("红外传感器动作")
        # 设备为人体传感器的 动作
        if a['deviceType']['deviceTypeId'] == 6 and a['deviceStat'] == '1':
            print("人体检测")
            GPIO.setup(gpio, GPIO.IN);
            if GPIO.input(gpio):
                time.sleep(0.01)
                # 二次过滤
                if GPIO.input(gpio):
                    flag2 += 1;
                    if flag2 < 2:
                        # 网址
                        url2 = "http://" + host + "/znjjPage/SendInfoServlet?stat=bodySensor"
                        # post 参数
                        pdata2 = {'deviceId': a['deviceId']}
                        pdata2 = urllib.parse.urlencode(pdata2)
                        binary_data2 = pdata2.encode('utf-8')
                        f = urllib.request.urlopen(url2, binary_data2)
                        data2 = f.read()
                        data2 = data2.decode('UTF-8')
                        if data2 == 'OK':
                            print("上传成功")
                        else:
                            print("上传失败")
                        print('Input was HIGH')
            else:
                flag2 = 0
                print("save")

    time.sleep(5)
