# -*- coding:utf-8 -*-
import cv2
import datetime
import dlib
import os
import json
import requests
import time
import sys
import random

from sftp_upload import sftp_upload

output_dir = './my_faces'
size = 160

host = '121.69.75.194'  # 主机
port = 22  # 端口
username = 'wac'  # 用户名
password = '8112whz'  # 密码
local = '/Users/ngxin/facerecognition/client/face_recognition/my_faces'
remote = '/home/wac/ngxin/ftp_upload/'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
#获取mac地址

def get_mac_address():
    import uuid
    node = uuid.getnode()
    mac = uuid.UUID(int=node).hex[-12:]
    return mac

detector = dlib.get_frontal_face_detector()
camera = cv2.VideoCapture(0)
index = 1
while True:

    print('Being processed picture %s' % index)
    frame, img = camera.read()
    cv2.imshow('face', img)
    if (index % 3 == 0):
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        dets = detector(gray_img)

        for i, d in enumerate(dets):
            add = 25
            x1 = d.top() if d.top() > 0 else 0
            y1 = d.bottom() if d.bottom() > 0 else 0
            x2 = d.left() if d.left() > 0 else 0
            y2 = d.right() if d.right() > 0 else 0
            #rect = cv2.rectangle(img, (x2-add, x1-add), (y2+add ,  y1+add), (0, 0, 255),2)
            rect = cv2.rectangle(img, (x2, x1), (y2 ,  y1), (0, 0, 255),2)

            face = img[x1:y1,x2:y2]
            face = cv2.resize(face, (size,size))

            cv2.imshow('face', img)
            cur_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
            mac_addr = get_mac_address()
            cv2.imwrite(output_dir + '/' + mac_addr + cur_time+str(index) + str(i) + '.jpg', face)
            #sftp_upload(host, port, username, password, local, remote)
            message_search = {"id": "weibo",
                              "pics": [{
                                           "path": output_dir + '/' + mac_addr + cur_time+str(index) + str(i) + '.jpg',
                                           "id": cur_time, "consume_history": "True"}]
                              }
            temp = json.dumps(message_search)
            payloadfiles = {'files': temp}

            start = time.time()
            r = requests.post("http://0.0.0.0:3006/query", data=payloadfiles)
            print time.time() - start
            print r.text
    index += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
