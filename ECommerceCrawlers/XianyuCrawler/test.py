from dingtalkchatbot.chatbot import DingtalkChatbot



# -*- coding: utf-8 -*-
import requests,json

#消息内容,url地址
def dingtalk(msg,webhook):
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    data = {'msgtype': 'text', 'text': {'content': msg}, 'at': {'atMobiles': [], 'isAtAll': False}}
    post_data = json.dumps(data)
    response = requests.post(webhook, headers=headers, data=post_data)
    return response.text



webhook = 'https://oapi.dingtalk.com/robot/send?access_token=aaa02da492d2b30f1955f1cecffca296dc9a1c4ba1c872b9bc9b7fdbfa7992f6'
print(dingtalk("msg test",webhook))



webhook2 = 'https://oapi.dingtalk.com/robot/send?access_token=你机器人的token'

xiaoding = DingtalkChatbot(webhook2)

xiaoding.send_text(msg="我就是我, 是不一样的烟火")