#!/usr/bin/env python
#coding:utf-8
import rospy
import datetime
from twitter import Twitter, OAuth
from cs_connection.msg import PrintStatus

access_token = "1186213676241391618-Ysqy92HV27PUA5D5Py144uKQxovNnf"
access_token_secret = "NgRByY4JgyaQ96AalP3t6b9OnlnvDOsY0XpNdkgaQ15lc"
api_key = "qxFknqYqOF9amjYgPAixlKr6V"
api_secret = "6hMTJPgycJCTIOynAiK7GYtFzfWgSgQj1dtch0IeD47zOMzLYg"
tweet = Twitter(auth = OAuth(access_token, access_token_secret, api_key, api_secret))

text = 'ros'

coat_msg = ["赤コート  ","青コート  "]
fight_msg = ["予選ムーブ\n","決勝ムーブ\n"]

status_msg = ["ただいまスタートゾーンから出発しました。\n",
"バスタオル１枚目を干しに行きます。\n",
"バスタオル２枚目を干しに行きます。\n",
"シーツを干しに行きます。\n",
"バスタオル１枚目を干し終わりました。\n",
"バスタオル２枚目を干し終わりました。\n",
"シーツを干し中です\n",
"シーツを干し終わりました。\n",
"スタートゾーンに戻ります。\n",
"スタートゾーンに到着しました。\n"]

#def callback(data):
#    rospy.loginfo(rospy.get_caller_id() + "get %s",data.data)


def twitter_send(data):
    dt_now = datetime.datetime.now()
    date = dt_now.strftime('%m月%d日 %H時%M分')
    send_status = status_msg[0]
    rospy.loginfo("status : %d",data.status)
    if data.status == 1:
        send_status = status_msg[0]
    elif data.status == 5:
        if data.towel1:
            send_status = status_msg[1]
        elif data.towel2:
            send_status = status_msg[2]
    elif data.status == 10:
        send_status = status_msg[3]
    elif data.status == 7:
        if data.towel1:
            send_status = status_msg[4]
        elif data.towel2:
            send_status = status_msg[5]
    elif data.status == 12:
        send_status = status_msg[6]
    elif data.status == 15:
        send_status = status_msg[7]
    elif data.status == 18:
        send_status = status_msg[8]
    elif data.status == 21:
        send_status = status_msg[9]
    else:
        return

    text = date + "\n明石高専自動機からお伝えします。\n練習中\n" + coat_msg[data.coat] + fight_msg[data.fight] + send_status + "#ロボコン\n" + "#明石高専\n" + "#AkashiSuperDry"
    print(text)
    # 生の投稿データの出力
    statusUpdate = tweet.statuses.update(status=text)
    print(statusUpdate)

    # 要素を絞った投稿データの出力
    print(statusUpdate['user']['screen_name'])
    print(statusUpdate['user']['name'])
    print(statusUpdate['text'])

def init():
    rospy.init_node('twitter_node')
    rospy.Subscriber("print_status",PrintStatus,twitter_send)
    rospy.loginfo("twitter node start")
    rospy.spin()

if __name__=='__main__':
    try:
        init()
    except rospy.ROSInterruptException: pass
