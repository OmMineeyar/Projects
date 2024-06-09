import numpy as np
import requests
import serial
import cv2
import time
data=open("c:/Users/AISHWARYA/Downloads/S.txt","r")
f=data.read()
deliminters=[' ','|']
for i in deliminters:
    f=f.replace(i,' ')
result=f.split()
print(len(result))
for i in range (len(result)):
    result[i]=int(result[i])
print(result)
result=np.array(result)
# Replace with your ESP32 IP address
esp32_ip = "192.168.51.136"

print(result)
result1 = result.copy()
result1 = np.reshape(result1,(67,48,3))
print(result1)
result1= result1.astype(np.uint8)
result1 = cv2.cvtColor(result1 , cv2.COLOR_RGB2BGR,result1)

cv2.imshow("img",result1)
cv2.waitKey()
result0 = result.copy()
k=6
for c in range (6):
    result=result0[c*(1584):(c+1) * (1584)]
    data_string = ",".join(map(str, result.flatten()))
    # data_string11
    # print(da)
    url = f"http://{esp32_ip}/send-array"
    data_string = str(c) + data_string
    data = {"data": data_string}
    response = requests.post(url, data=data)

# result=result[3216:-3216]

print(response.text)