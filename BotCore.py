import base64
import datetime
import json
import os
import random
import re
import threading
import time
from time import sleep
import datetime
import iotbot.decorators as deco
import requests
import schedule
from iotbot import IOTBOT, Action, GroupMsg

from Utils import utils, SQLiteUtils, BaiduApi, setuUtil, ciyunUtil
from chatPlugin import main
day = datetime.date.today().strftime("%Y%m%d")
bot = IOTBOT(1328382485, log_file_path='log/' + day + '.log')
action = Action(bot)


def getGroupList():
    GroupID = []
    groupList = action.get_group_list()
    TroopList = groupList['TroopList']
    for group in TroopList:
        GroupID.append(group['GroupId'])
    return GroupID


def sent_wyy():
    print("网抑云定时任务执行成功")
    file = os.listdir('wyy')[random.randint(0, 9)]
    groupList = getGroupList()
    text = SQLiteUtils.get_netease()
    with open('wyy//' + file, 'rb') as f:
        coding = base64.b64encode(f.read()).decode()
        for group in groupList:
            action.send_group_pic_msg(toUser=group, content=text, picBase64Buf=coding)
            sleep(1)
    return


def sent_morning():
    print("早安定时任务执行成功")
    file = os.listdir('morning')[random.randint(0, 10)]
    text = SQLiteUtils.get_morning()
    groupList = getGroupList()
    print(text)
    with open('morning//' + file, 'rb') as f:
        coding = base64.b64encode(f.read()).decode()
        for group in groupList:
            action.send_group_pic_msg(toUser=group, content=text, picBase64Buf=coding)
            sleep(1)
    return


def sent_ciyun():
    print("开始生成词云")
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = (today - oneday).strftime("%Y%m%d")  # 昨天的日期
    groupList = getGroupList()
    for group in groupList:
        filename = group + '_' + yesterday + '.txt'
        pic_base64 = ciyunUtil.create_ciyun(filename)
        action.send_group_pic_msg(toUser=group, content="昨日本群词云已生成，请查收~[PICFLAG]", picBase64Buf=pic_base64)
        # print(pic_base64)


def schedule_test():
    Content = time.asctime(time.localtime(time.time()))
    action.send_friend_text_msg(toUser=1127738407, content=Content)
    print("执行成功")


def schedule_threading():
    while True:
        schedule.run_pending()
        # print("refresh")
        sleep(1)


@bot.on_group_msg
def get_record(msg: GroupMsg):
    today = datetime.date.today().strftime("%Y%m%d")
    if msg.MsgType == 'TextMsg':
        filename = str(msg.FromGroupId) + '_' + today + '.txt'
        with open('record/' + filename, 'a')as f:
            f.write(msg.Content + '\n')
            f.close()

@bot.on_group_msg
@deco.only_this_msg_type("TextMsg")
def auto_reply(msg: GroupMsg):
    rand = random.randint(0, 20)
    print(rand)
    if rand % 15 == 0:
        question = msg.Content
        reply = main.chat(question)
        action.send_group_text_msg(msg.FromGroupId, reply, atUser=msg.FromUserId)


@bot.on_group_msg
@deco.in_content("色图")
@deco.not_these_groups([1146517332])
def send_setu(msg: GroupMsg):
    base_64 = setuUtil.get_setu()
    action.send_group_pic_msg(toUser=msg.FromGroupId, content='30S后销毁该消息，请快点冲，谢谢', picBase64Buf=base_64)


@bot.on_group_msg
def revoke_msg(msg: GroupMsg):
    if msg.FromUserId == 1328382485 and msg.MsgType == 'PicMsg':
        Content = json.loads(msg.Content)['Content']
        if Content == '30S后销毁该消息，请快点冲，谢谢':
            print(Content)
            time.sleep(30)
            action.revoke_msg(msg.FromGroupId, msg.MsgSeq, msg.MsgRandom)



@bot.on_group_msg
@deco.in_content("彩虹屁")
def send_chp(a: GroupMsg):
    text = utils.get_chp()
    print(text)
    action.send_group_text_msg(toUser=a.FromGroupId, content=text)


@bot.on_group_msg
@deco.in_content("文案")
def send_pyq(a: GroupMsg):
    text = utils.get_pyq()
    print(text)
    action.send_group_text_msg(toUser=a.FromGroupId, content=text)


@bot.on_group_msg
@deco.in_content("毒鸡汤")
def send_djt():
    text = utils.get_djt()
    print(text)
    action.send_group_text_msg(toUser=a.FromGroupId, content=text)


@bot.on_group_msg
def send_shanzhao(a: GroupMsg):
    if a.MsgType == 'PicMsg' and 'GroupPic' not in a.Content:
        Contents = json.loads(a.data.get('Content'))
        if a.FromGroupId == 1146517332:
            print("Get Message!")
            action.send_friend_pic_msg(toUser=1127738407, content='有人发闪照了~', picUrl=Contents['Url'],
                                       fileMd5=Contents['FileMd5'])
            with open('imgSave//' + str(int(time.time())) + '.jpg', 'wb')as f:
                res = requests.get(url=Contents['Url'])
                f.write(res.content)
            return
        else:
            action.send_group_pic_msg(toUser=a.FromGroupId, content='震惊！居然有人敢在这个群里发闪照！', picUrl=Contents['Url'],
                                      fileMd5=Contents['FileMd5'])
            return


@bot.on_group_msg
@deco.in_content("我想对你说")
def send_voice(a: GroupMsg):
    file_name = BaiduApi.text2audio()
    with open(file_name, 'rb') as f:
        coding = base64.b64encode(f.read())  # 读取文件内容，转换为base64编码
        print('本地base64转码~')
        voice_base64 = coding.decode()
        action.send_group_voice_msg(toUser=a.FromGroupId, voiceBase64Buf=voice_base64)
        return


@bot.on_group_msg
@deco.in_content("QQ测运势")
def send_qqcys(msg: GroupMsg):
    text = utils.get_cjx(msg)
    print(text)
    action.send_group_text_msg(toUser=msg.FromGroupId, content=text,atUser=msg.FromUserId)


@bot.on_group_msg
def send_xingzuo(a: GroupMsg):
    pattern = re.compile(r'#(.*?座)(.*?)运势')
    m = pattern.match(a.Content)
    if m is not None:
        text = utils.get_xzys(m.group(1), m.group(2))
        print(text)
        action.send_group_text_msg(toUser=a.FromGroupId, content=text)


if __name__ == "__main__":
    schedule.every().day.at("00:00").do(sent_wyy)
    schedule.every().day.at("08:00").do(sent_ciyun)
    schedule.every().day.at("07:00").do(sent_morning)
    thread_schedule = threading.Thread(target=schedule_threading)
    thread_schedule.start()
    bot.run()
