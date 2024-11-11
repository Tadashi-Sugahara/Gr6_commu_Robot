from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import os
import re

def text_to_speech(text):

    # テキストを言語ごとに分割
    segments = re.findall(r'[^\x00-\x7F]+|[\x00-\x7F]+', text)
    
    # 各セグメントを音声に変換して結合
    combined_audio = AudioSegment.empty()
    for segment in segments:
        if segment.strip():  # 空のセグメントを無視
            print(segment)
            lang = 'ja' if re.search(r'[^\x00-\x7F]', segment) else 'en'
            tts = gTTS(text=segment, lang=lang)
            tts.save("segment.mp3")
            segment_audio = AudioSegment.from_mp3("segment.mp3")
            # 音声を再生
            # 再生速度を変更 (1.5倍速)
            if lang == 'ja':
                tunning_speed = 1.2
            else:
                tunning_speed = 1.0
            new_frame_rate = int(segment_audio.frame_rate * tunning_speed)
            faster_audio = segment_audio._spawn(segment_audio.raw_data, overrides={'frame_rate': new_frame_rate})
            faster_audio = faster_audio.set_frame_rate(segment_audio.frame_rate)            
            play(faster_audio)


if __name__ == "__main__":
    # ユーザーからテキストデータを入力
    text = input("テキストを入力してください: ")
    text_to_speech(text)
