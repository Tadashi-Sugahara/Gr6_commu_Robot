import speech_recognition as sr

def speech_to_text():

    # Create a recognizer object
    r = sr.Recognizer()

    # Set the microphone as the audio source
    mic = sr.Microphone()

    # Adjust microphone sensitivity if needed
    # mic.adjust_for_ambient_noise()

    # Capture audio from the microphone
    # マイクから音声を取得
    with sr.Microphone() as source:
        print("Say something!")
        # ノイズの調整
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            # タイムアウトとフレーズの終了を検出するためのパラメータを設定
            audio = r.listen(source, timeout=20, phrase_time_limit=15)
            print("Audio captured successfully.")
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except sr.UnknownValueError:
            print("Could not understand audio")
        except Exception as e:
            print(f"An error occurred: {e}")

    # Convert speech to text
    try:
        text = r.recognize_google(audio, language="ja-JP")
        #print("Recognized text:", text)
        return text
    except sr.UnknownValueError:
        print("Unable to recognize speech (Time out)")
        return False
    except sr.RequestError as e:
        print("Error:", str(e))
        return False

if __name__ == "__main__":
    text = speech_to_text()
    print("Recognized text:", text)