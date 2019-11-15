#!/usr/bin/env python
#coding:utf-8
import rospy
import datetime
import json
import time
import os
import subprocess
#from twitter import Twitter, OAuth
from requests_oauthlib import OAuth1Session
from cs_connection.msg import PrintStatus
from sensor_msgs.msg import Image
from std_msgs.msg import String

access_token = "1186213676241391618-Ysqy92HV27PUA5D5Py144uKQxovNnf"
access_token_secret = "NgRByY4JgyaQ96AalP3t6b9OnlnvDOsY0XpNdkgaQ15lc"
api_key = "qxFknqYqOF9amjYgPAixlKr6V"
api_secret = "6hMTJPgycJCTIOynAiK7GYtFzfWgSgQj1dtch0IeD47zOMzLYg"

url_media = "https://upload.twitter.com/1.1/media/upload.json"
url_text = "https://api.twitter.com/1.1/statuses/update.json"

#tweet = Twitter(auth = OAuth(access_token, access_token_secret, api_key, api_secret))
#OAuth認証 セッション開始
twitter = OAuth1Session(api_key, api_secret, access_token, access_token_secret)

text = 'ros'

coat_msg = ["赤コート  ","青コート  "]
fight_msg = ["予選ムーブ\n","決勝ムーブ\n"]

def twitter_send(data):
    dt_now = datetime.datetime.now()
    date = dt_now.strftime('%m月%d日 %H時%M分%S秒')
    img_ok = True
    send_status = "動作なし\n"
    img_path = "start.jpg"
    rospy.loginfo("status : %d",data.status)
    if data.status == 1:
        send_status = "ただいまスタートゾーンから出発しました。\n"
        img_path = "start.jpg"
    elif data.status == 5:
        img_ok = False
        if data.towel1:
            send_status = "バスタオル１枚目を干しに行きます。\n"
        else:
            send_status = "バスタオル２枚目を干しに行きます。\n"
    elif data.status == 10:
        img_ok = False
        send_status = "シーツを干しに行きます。\n"
    elif data.status == 7:
        img_path = "bathtowel.jpg"
        if data.towel1:
            send_status = "バスタオル１枚目を干し終わりました。\n"
        else:
            send_status = "バスタオル２枚目を干し終わりました。\n"
    elif data.status == 12:
        img_ok = False
        send_status = "シーツを干し中です。\n"
    elif data.status == 15:
        img_path = "sheets.jpg"
        send_status = "シーツを干し終わりました。\n"
    elif data.status == 18:
        img_ok = False
        send_status = "スタートゾーンに戻ります。\n"
    elif data.status == 21:
        img_path = "arrival.jpg"
        send_status = "スタートゾーンに到着しました。\n"
    else:
        return

    text = date + "\n明石高専自動機からお伝えします。\n練習中\n" + coat_msg[data.coat] + fight_msg[data.fight] + send_status + "#ロボコン\n" + "#明石高専\n" + "#AkashiSuperDry"
    print(text)
    # 生の投稿データの出力
    media_id = 0
    param = {'status' : text}
    start_time = time.time()
    while not os.path.isfile(img_path) and img_ok:
        if time.time() - start_time > 2:
            print("画像ファイルなし")
            img_ok = False
            break
    
    if img_ok:
        img_data = {'media' : open(img_path, 'rb')}
        req_media = twitter.post(url_media, files = img_data)
        if req_media.status_code != 200:
            print("画像アップロード失敗 : "+ req_media.text)
        else:
            print("画像アップロード成功 : "+ req_media.text)
            media_id = json.loads(req_media.text)['media_id']
            print('media_id:%d'% media_id)
            param['media_ids'] = [media_id]

    req_media = twitter.post(url_text, params = param)
    args = ['rm','-f',img_path]
    try:
        res = subprocess.check_call(args)
        print(res)
    except:
        print("cannot remove : " + img_path)
    #statusUpdate = tweet.statuses.update(status=text)
    #print(statusUpdate)

    # 要素を絞った投稿データの出力
    #print(statusUpdate['user']['screen_name'])
    #print(statusUpdate['user']['name'])
    #print(statusUpdate['text'])

def init():
    rospy.init_node('twitter_node')
    rospy.Subscriber("print_status",PrintStatus,twitter_send)
    rospy.loginfo("twitter node start")
    rospy.spin()

if __name__=='__main__':
    try:
        init()
    except rospy.ROSInterruptException: pass
