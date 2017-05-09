import urllib.request
import urllib
import json

import time

# 网址
url2 = "http://localhost:8080/znjj/SendInfoServlet?stat=temp"
# post 参数
pdata2 = {'temperature': 30, 'humidity': 70, 'deviceId':4}
pdata2 = urllib.parse.urlencode(pdata2)
binary_data2 = pdata2.encode('utf-8')
f = urllib.request.urlopen(url2, binary_data2)
data2 = f.read()
data2 = data2.decode('UTF-8')
print(data2)
