# -*- coding: utf-8 -*-
import json
import datetime
import time
import urllib
import re
import requests
import random
import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#解析B站动态网址ID
s = input("请输入B站动态网址：")
nums = re.findall(r'\d+', s)
Dynamic_id = str(nums[0])
print("动态ID为：" + Dynamic_id)
DynamicAPI = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id=" + Dynamic_id

#使用B站API发送请求获取Json数据
res = requests.get(DynamicAPI)
BiliJson = json.loads(str(res.content, encoding = "utf-8"))
Total_count = BiliJson['data']['card']['desc']['repost']
UP_UID = BiliJson['data']['card']['desc']['user_profile']['info']['uid']
print("该动态UP主ID：" + str(UP_UID))
print("转发总数为：" + str(Total_count))
Tmp_count = 0
unameList = []
DynamicAPI = "https://api.live.bilibili.com/dynamic_repost/v1/dynamic_repost/view_repost?dynamic_id="+ Dynamic_id + "&offset="

for x in range (0,5):  
    b = "抓取转发用户ID" + "." * x
    print (b, end="\r")
    time.sleep(1)

#分页获取转发动态账号
while Tmp_count < Total_count:
    #print(str(Tmp_count)*10, end='')
    #sys.stdout.flush()
    #获取当前页面的评论
    Tmp_DynamicAPI = DynamicAPI + str(Tmp_count)
    res = requests.get(Tmp_DynamicAPI)
    BiliJson = json.loads(str(res.content, encoding = "utf-8"))
    memberList = BiliJson["data"].get('comments')
    for x in memberList:
        print(x['uname'])
        unameList.append(x['uname'])
    Tmp_count = Tmp_count + 20

#去除重复账号
print("\n删除重复账号...\n")
unameList = list(set(unameList)) 

#删除up主自己
print("删除UP主账号:" + bcolors.OKGREEN + "秦无邪OvO" + bcolors.ENDC + "\n")
if '秦无邪OvO' in unameList:
    unameList.remove("秦无邪OvO") 
#for uname in unameList:
#    print(uname)

print("------开始随机抽奖过程------")
#开始随机抽奖过程
prizeQuantity = 2 #设置奖品数量
for i in range(prizeQuantity):
    biliID = random.choice(unameList)
    for x in range (0,4):  
        b = "抽奖中" + "." * x
        print (b, end="\r")
        time.sleep(1) 
    #print(f"{bcolors.OKGREEN}Warning: No active frommets remain. Continue?{bcolors.ENDC}")   
    print("第" + bcolors.OKGREEN + str(i+1) + bcolors.ENDC + "位中奖用户：" + bcolors.OKGREEN + biliID + bcolors.ENDC)
    unameList.remove(biliID) #防止重复抽取同一人
print("------抽奖过程结束------")

print("\n抽奖名单统计完毕！\n")

