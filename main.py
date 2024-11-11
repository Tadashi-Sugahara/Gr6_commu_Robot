# 2024/8/26 更新

from openai import AzureOpenAI
import os
import dotenv
import requests
import base64
import serial
from alarm_text2audio import text_to_speech
from alarm_audio2text import speech_to_text
from ai_camera import ai_camera
from ai_face_auth import ai_face_auth
from ai_talk import talk
from ai_translate import translate

import datetime
import time

# =============================================== #
# 1分ごとに処理を行うために、時刻の分が変わるとTrueを返す
# =============================================== #
def minuteChanged():
    # 現在の時刻を取得
    current_minute = datetime.datetime.now().minute
    while True:
        if datetime.datetime.now().second == 0:
            time.sleep(1)
            print("00秒を検知")
            return True
        else:
            print("00秒以外")
            return False

# =============================================== #
# サーバから設定時間を取得してjson形式で返す
# =============================================== #
def getTime():
    print("ユーザが設定した時間をサーバのDBから取得します")

    # データの取得 
    url = "https://ai-alarm-webapp.vercel.app/api/setTime"
    response = requests.get(url)
    if response.status_code == 200:
        print("res ok. Data:",response.json())
        return response.json()
    else:
        print("Failed to retrieve data from the API")

# =============================================== #
# 設定時間と現在の時間を比較して一致していたら True を返す
# =============================================== #
def timeCheck(setTime):
    # データが空でないかチェック
    if setTime is None:
        print("No data to check")
        return False

    # 現在時刻を取得してhh:mmに変換
    currentTime = datetime.datetime.now()
    nowTime = currentTime.strftime("%H:%M")

    # 辞書のキーを使用してアクセス
    if 'data' in setTime and isinstance(setTime['data'], list) and len(setTime['data']) > 0:
        webAppSetTime = (setTime['data'][0]['settingTime'])
        print("webAppSetTime:",webAppSetTime)
        print("nowTime:", nowTime)

        if webAppSetTime == nowTime:
            print("設定時刻と現在時刻一致")
            return True
        else:
            print("設定時刻と現在時刻時刻一致せず")
            return False
    else:
        print("Invalid data format")
        return False


def main():
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)


    #ser.open()
    print("Serial port opened")
    
    send_data = '0'
    ser.write(send_data.encode())
    
    while(1):
        rcv = ser.read(1)
        data = rcv.decode()
        print(data)
        
        if data == '9':
            send_data = '2'
            ser.write(send_data.encode())
            text_to_speech("いらっしゃいませ")
            text_to_speech("なにか、英語通訳のお手伝いしますか？")
            text_to_speech("お話の話題の提案は、スイッチ０を押してください。")
            send_data = '3'
            ser.write(send_data.encode())
        
        if data == '7':
            send_data = '2'
            ser.write(send_data.encode())
            topic = "今日は何の日"  # ここでトピックを自由に指定できます
            talk(topic)
            send_data = '3'
            ser.write(send_data.encode())
        
        if data == '8':
            send_data = '2'
            ser.write(send_data.encode())
            translate()
            send_data = '3'
            ser.write(send_data.encode())
    ser.close()


if __name__ == "__main__":
    
    main()
    

