#coding=utf-8
import requests
import json
import time


message_search = { "id" : "weibo_3992350184721547",
            "pics" : [ {"path":  "/Users/Lavector/git-back/facerecognition/server/data/AfterTheSunSet_004119160_00000011.png", "id" : "b9c7afaf2edda3cc5011dfcd07e93901233f9253", "consume_history": "True"}]
}

message_add = { "id" : "weibo_3992350184721547",
            "pics" : [ {"path": "/Users/Lavector/git-back/facerecognition/server/data/7.png", "id" : "b9c7afaf2edda3cc5011dfcd07e93901233f9254", "consume_history": "True"}]
}



temp =  json.dumps(message_search)
payloadfiles = {'files':temp}

start = time.time()
r = requests.post("http://0.0.0.0:3006/query",data=payloadfiles)
print time.time() - start
print r.text
# for i in range(50):
#     start = time.time()
#     r = requests.post("http://0.0.0.0:3005/search",data=payloadfiles)
#     print i, time.time() - start
    # print r.text

# temp =  json.dumps(message_add)
# payloadfiles = {'files':temp}
# start = time.time()
# r = requests.post("http://0.0.0.0:3005/add",data=payloadfiles)
# print time.time() - start
# print r.text



# import json
#
# total = 0.0
# num = 0
# f = open('../es_image_search.json', 'r')
# for line in f.readlines():
#     num += 1
#     if num > 1000:
#         break
#     # if num < 94443:
#     #     continue
#     data = json.loads(line)['_source']
#     message = {}
#     message['id'] = data['msg_id']
#     message_pic = {}
#     message_pic['url'] = data['path']
#     message_pic['id'] = data['pic_id']
#     message['pics'] = [message_pic]
#
#     payloadfiles = {'files': json.dumps(message)}
#     start = time.time()
#     r = requests.post("http://0.0.0.0:3005/search", data=payloadfiles)
#     cost = time.time() - start
#     print cost
#     print num, message_pic['url'], r.text
#     total += cost
#
# f.close()
# print 'cost:%f'%(total/num)

# num = 0
# f = open('../es_image_search.json','r')
# for line in open('../es_image_search.json','r'):
#     line = f.readline()
#     print line
#     num += 1
# print num
