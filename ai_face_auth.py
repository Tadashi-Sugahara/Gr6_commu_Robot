from openai import AzureOpenAI
import os
import dotenv
import requests
import base64
import cv2

def capture_photo_face_auth(mode):
    # Connect to the USB camera
    camera = cv2.VideoCapture(0)

    # Check if the camera is opened successfully
    if not camera.isOpened():
        print("Failed to open the camera")
        return

    # Capture a photo
    ret, frame = camera.read()

    # Check if the photo is captured successfully
    if not ret:
        print("Failed to capture the photo")
        return

    # フレームをJPEG形式にエンコード
    ret, jpeg = cv2.imencode('.jpg', frame)
    if not ret:
        print("フレームをJPEG形式にエンコードできませんでした")
        camera.release()
        exit()

    # Release the camera
    camera.release()

    if mode == 0:
        # Encode the photo to base64
        encoded_image = base64.b64encode(jpeg).decode("utf-8")

        return encoded_image
    
    elif mode ==1:
        cv2.imwrite('image/face_image.jpg', frame) 

        return True


def ai_face_auth():
    # Call the capture_photo function before sending the payload
    headers = {
        "Content-Type": "application/json",
        "api-key": os.environ['AZURE_OPENAI_KEY'],
    }
    # ペイロード
    with open('image/face_image.jpg', 'rb') as f:
        jpeg1 = base64.b64encode(f.read()).decode("utf-8")
    image_url1 = f"data:image/jpeg1;base64,{jpeg1}"
    image_url2 = f"data:image/jpeg2;base64,{capture_photo_face_auth(0)}"
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
                    "text": "2枚の画像に映っているのが同一人物か教えてください。" #\
                             #同一人物の場合は、文字列の1を、\
                             #異なる人物または半断できない場合は、文字列の0を返してください。"
                    },
                    {
                    "type": "image_url",
                    "image_url":{
                        "url": image_url1
                    }
                    },
                    {
                    "type": "image_url",
                    "image_url":{
                        "url": image_url2
                    }
                    }
                ]
            }
        ],
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 800
    }

    azure_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"] + "openai/deployments/" + os.environ["AZURE_OPENAI_DEPLOYMENT"] + "/chat/completions?api-version=2024-02-15-preview"

    try:
        response = requests.post(azure_endpoint, headers=headers, json=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Request failed:")
        raise SystemExit(e)

    response_json = response.json()
    assistant_message = response_json['choices'][0]['message']['content']

    return assistant_message


def main():
    dotenv.load_dotenv()
    #登録用の顔画像を撮影する
    capture_photo_face_auth(1)
    #登録用の顔画像と一致しているか判定し、結果を返す
    assistant_message = ai_face_auth()
    print(f"AzuleAIの返答: {assistant_message}")


if __name__ == "__main__":
    main()
