# -*- coding: utf-8 -*-#
from aip import AipSpeech
import requests
import json
import speech_recognition as sr
import win32com.client
import pygame
import pyaudio
import pyttsx3
from flask import Flask,render_template
import time  # 导入此模块，获取当前时间
import threading
from ceshi import cn2dig
app = Flask(__name__)

# 初始化语音
speaker = win32com.client.Dispatch("SAPI.SpVoice")
engine = pyttsx3.init()  # 初始化语音库
# 设置语速
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-50)

# 1、语音生成音频文件,录音并以当前时间戳保存到voices文件中
# Use SpeechRecognition to record 使用语音识别录制
def my_record(rate=16000):
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=rate) as source:
        print("please say something")
        speaker.Speak("请您说出您的问题")
        audio = r.listen(source)

    with open("C:\\Users\87253\PycharmProjects\YYshibie\\voices\myvoices.wav", "wb") as f:#按照这格式自行改本地路径
        f.write(audio.get_wav_data())


# 2、音频文件转文字：采用百度的语音识别python-SDK
# 导入我们需要的模块名，然后将音频文件发送给出去，返回文字。
# 百度语音识别API配置参数
APP_ID = '21182611'
API_KEY = 'jlGviUkPLHnR3PoHhX3Am7RQ'
SECRET_KEY = 'PQGt4jEMNQbGN7UOH2rYVXPkaDHBGzVG'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
path = 'C:\\Users\87253\PycharmProjects\YYshibie\\voices\myvoices.wav'#按照这格式自行改本地路径
musicPath = r"C:\CloudMusic\易烊千玺 - 宝贝.mp3"#自行改本地歌曲路径

#播放音乐
def yinyue(musicPath):
    pygame.mixer.init()  # 初始化
    pygame.mixer.music.load(musicPath)  # 加载音乐
    pygame.mixer.music.play()  # 播放
    track = musicPath.split('\\')
    line = track[2].split('.')[0]
    return line

#闹钟功能
def naozhong(request):
    # 提示用户设置时间和分钟
    request_1 = request[2:]
    if request_1[0]=='，':
        request_1 = request_1[1:]
    my_hour = request_1.split('点')[0]
    my_minute = request_1.split('点')[1].split('分')[0]
    # my_hour = cn2dig(request_1.split('点')[0])
    # my_minute = cn2dig(request_1.split('点')[1][0])
    flag = 1
    while flag:
        t = time.localtime()  # 当前时间的纪元值
        fmt = "%H %M"
        now = time.strftime(fmt, t)  # 将纪元值转化为包含时、分的字符串
        now = now.split(' ')  # 以空格切割，将时、分放入名为now的列表中
        hour = now[0]
        minute = now[1]
        if hour == my_hour and minute == my_minute:
            speaker.Speak("时间到时间到时间到时间到时间到时间到时间到时间到时间到时间到时间到时间到")
            flag = 0

# 将语音转文本STT
def listen():
    # 读取录音文件
    with open(path, 'rb') as fp:
        voices = fp.read()
    try:
        # 参数dev_pid：1536普通话(支持简单的英文识别)、1537普通话(纯中文识别)、1737英语、1637粤语、1837四川话、1936普通话远场
        result = client.asr(voices, 'wav', 16000, {'dev_pid': 1537, })
        result_text = result["result"][0]
        print("you said: " + result_text)
        return result_text
    except KeyError:
        print("KeyError")
        engine.say("我没有听清楚，请再说一遍...")
        engine.runAndWait()

# 3、与机器人对话：调用的是图灵机器人
# 图灵机器人的API_KEY、API_URL
#turing_api_key = "***"
turing_api_key = "***"
api_url = "http://openapi.tuling123.com/openapi/api/v2"  # 图灵机器人api网址
headers = {'Content-Type': 'application/json;charset=UTF-8'}


# 图灵机器人回复
def Turing(text_words=""):
    req = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": text_words
            },

            "selfInfo": {
                "location": {
                    "city": "北京",
                    "province": "北京",
                    "street": "车公庄"
                }
            }
        },
        "userInfo": {
            "apiKey": turing_api_key,  # 你的图灵机器人apiKey
            "userId": "bb"  # 用户唯一标识(随便填, 非密钥)
        }
    }

    req["perception"]["inputText"]["text"] = text_words
    response = requests.request("post", api_url, json=req, headers=headers)
    response_dict = json.loads(response.text)

    result = response_dict["results"][0]["values"]["text"]
    print("AI Robot said: " + result)
    return result


@app.route('/')
def index():
  return render_template('my-link.html')
@app.route('/tap/')
def tap():
    return render_template('template.html')
@app.route('/my-link/')
def my_link():
    my_record()
    request = listen()
    if (request[0]=="闹"):
        t_naozhong = threading.Thread(target=naozhong, args=(request,))
        t_naozhong.start()
        speaker.Speak("设置闹钟成功啦！")
        context = {
            'wenti': request,
            'huida': '闹钟设置成功!'
        }
        return render_template('template.html',**context)
    else:
        if(request=="播放音乐。"):
            response = yinyue(musicPath)
        else:
            response = Turing(request)
        data = response
        context = {
            'wenti': request,
            'huida': data
        }
        speaker.Speak(data)
        return render_template('template.html',**context)
if __name__ == '__main__':
    app.run()
