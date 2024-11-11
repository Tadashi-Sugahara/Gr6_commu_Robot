from openai import AzureOpenAI
import os
import dotenv
import requests
import base64
from alarm_text2audio import text_to_speech
from alarm_audio2text import speech_to_text
from ai_camera import ai_camera
from ai_face_auth import ai_face_auth


# =============================================== #
# 英会話の話始めをサポートする
# =============================================== #
def talk(topic):
    dotenv.load_dotenv()    

    headers = {
        "Content-Type": "application/json",
        "api-key": os.environ['AZURE_OPENAI_KEY'],
    }
    # 初期のペイロード
    payload = {
        "messages": [
            {
                "role": "system",
                "content": [
                    {
                    "type": "text",
                    "text": "You are an AI assistant that helps people find information."
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": f"英会話の取り掛かりをサポートしてあげてください。\
                             {topic}は英語で何というか、そして{topic}に関する話初めの一文を答えてください。\
                             説明は日本語、例文は英語で回答してください。\
                             例文は話始めの一文だけで大丈夫です。\
                             説明も短めにしてください。\
                             最後に励ます言葉を短くかけてあげてください。\
                             返答には記号を入れないでください。\
                             会話の中で日本語を話すときは、親しみやすくフランクな言い方をしてください。"
                    }
                ]
            }
        ],
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 800
    }

    azure_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"] + "openai/deployments/" + os.environ["AZURE_OPENAI_DEPLOYMENT"] + "/chat/completions?api-version=2024-02-15-preview"

    while True:
        camera_res = ai_camera()

        if camera_res == '1':
            print("Face authentication successful")
            break
        try:
            response = requests.post(azure_endpoint, headers=headers, json=payload)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Request failed:")
            raise SystemExit(e)

        response_json = response.json()
        assistant_message = response_json['choices'][0]['message']['content']
        print(f"AzuleAIの返答: {assistant_message}")
        text_to_speech(assistant_message)
        break

        # AzuleAIの返答をペイロードに追加
        payload['messages'].append({
            "role": "assistant",
            "content": [
                {
                "type": "text",
                "text": assistant_message
                }
            ]
        })

        # ユーザーの入力を受け取る
        # user_input = input("あなたの回答: ")
        user_input = speech_to_text()
        if user_input != False:
            payload['messages'].append({
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": user_input
                    }
                ]
            })

if __name__ == "__main__":

    talk()
