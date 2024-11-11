#include <Arduino.h>
#include <Servo.h>


#ifndef PIN_BUZZER
#define PIN_BUZZER    A0
#endif

// 超音波センサのピン設定
const int ultrasonicPin = 3; 
// ブザーのピン設定
uint8_t const pin_buzzer = PIN_BUZZER;
// モーター端子定義
const int motorPin8 = 8;
const int motorPin9 = 9;
const int motorPin10 = 10;
const int motorPin11 = 11;

// 超音波センサで測定する障害物の距離限界 (cm)
const long limit_dist = 15;

// ユーザースイッチの設定
const int switchPin20 = 20; // GP20
const int switchPin21 = 21; // GP21
int switchState20 = 0;      // スイッチの状態を保存する変数
int switchState21 = 0;
int flag0 = 0;
int flag1 = 0;

// サーボモータの設定
Servo servo;

#define NOTE_C4  262
#define NOTE_CS4 277
#define NOTE_D4  294
#define NOTE_DS4 311
#define NOTE_E4  330
#define NOTE_F4  349
#define NOTE_FS4 370
#define NOTE_G4  392
#define NOTE_GS4 415
#define NOTE_A4  440
#define NOTE_AS4 466
#define NOTE_B4  494
#define NOTE_C5  523
#define NOTE_CS5 554
#define NOTE_D5  587
#define NOTE_DS5 622
#define NOTE_E5  659
#define NOTE_F5  698
#define NOTE_FS5 740
#define NOTE_G5  784
#define NOTE_GS5 831
#define NOTE_A5  880
#define NOTE_AS5 932
#define NOTE_B5  988

#define WHOLE         2200       // Length of time in milliseconds of a whole note (i.e. a full bar).
#define HALF          WHOLE/2
#define QUARTER       HALF/2
#define EIGHTH        QUARTER/2
#define EIGHTH_TRIPLE QUARTER/3
#define SIXTEENTH     EIGHTH/2


void playNote(int frequency, int duration, bool hold = false, bool measure = true) {
  (void) measure;

  if (hold) {
    tone(pin_buzzer, frequency, duration + duration / 32);
  } else {
    tone(pin_buzzer, frequency, duration);
  }

  delay(duration + duration / 16);
}

// 起動音
void wakeupMusic() {
  // Play a little charge melody, from:
  //  https://en.wikipedia.org/wiki/Charge_(fanfare)
  // Note the explicit boolean parameters in particular the measure=false
  // at the end.  This means the notes will play without any breath measurement
  // logic.  Without this false value playNote will try to keep waiting for candles
  // to blow out during the celebration song!
  playNote(NOTE_G4, EIGHTH_TRIPLE, true, false);
  playNote(NOTE_C5, EIGHTH_TRIPLE, true, false);
  playNote(NOTE_E5, EIGHTH_TRIPLE, false, false);
  playNote(NOTE_G5, EIGHTH, true, false);
  playNote(NOTE_E5, SIXTEENTH, false);
  playNote(NOTE_G5, HALF, false);

  return;
}

long SS_sens1(){
  long duration, distance;

  pinMode(ultrasonicPin, OUTPUT); // 最初は送信モードに設定
  // 超音波信号を送信
  digitalWrite(ultrasonicPin, LOW); // 送信前にピンをLOWに設定
  delayMicroseconds(2); // 2マイクロ秒待つ
  digitalWrite(ultrasonicPin, HIGH); // HIGHにして信号を送信
  delayMicroseconds(10); // 10マイクロ秒待つ
  digitalWrite(ultrasonicPin, LOW); // 送信終了
  
  // 受信モードに切り替え
  pinMode(ultrasonicPin, INPUT);
  
  // 超音波が反射して戻ってくるまでの時間を計測
  duration = pulseIn(ultrasonicPin, HIGH);
  
  // 距離を計算 (音速 = 343m/s、音速の半分を使用して計算)
  distance = (duration / 2) / 29.1;

  /*
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println("cm");
*/
  return distance;
}

// 前進
void moveFoward(int speed) {
  long distance;

  analogWrite(motorPin9, 0);
  analogWrite(motorPin10, 0);

/*
  analogWrite(motorPin8, speed-10);
  analogWrite(motorPin11, speed);
*/
  delay(1500);
  
  // 超音波センサで距離を測定
  distance = SS_sens1();
  delay(100);

  while (distance > limit_dist ){
    analogWrite(motorPin8, speed);
    analogWrite(motorPin11, speed);
    distance = SS_sens1();
    delay(100);
  }

  analogWrite(motorPin8, 0);
  analogWrite(motorPin11, 0);
  return;
}

// 後退
void moveBackward(int speed) {
  long distance;

  analogWrite(motorPin8, 0);
  analogWrite(motorPin11, 0);
  
  /*
  // 超音波センサで距離を測定
  distance = SS_sens1();
  delay(100);

  while (distance > limit_dist ){
    analogWrite(motorPin9, speed);
    analogWrite(motorPin10, speed);
    distance = SS_sens1();
    delay(100);
  }

  */
  analogWrite(motorPin9, speed);
  analogWrite(motorPin10, speed);
  delay(3000);
  
  analogWrite(motorPin9, 0);
  analogWrite(motorPin10, 0);

  return;
}

// 首振り
void shakingHead() {
  int servoPos = 0;
  
  for(servoPos = 0; servoPos <=180; servoPos +=30){
    servo.write(servoPos);
    delay(100);
  }

  for(servoPos = 180; servoPos >=0; servoPos -=30){
    servo.write(servoPos);
    delay(100);
  }
}


void setup() {
  Serial.begin(9600); // シリアル通信を9600bpsで開始

  // ブザー関連設定
  pinMode(pin_buzzer, OUTPUT);
  digitalWrite(pin_buzzer, LOW);

  // モータ関連の設定
  pinMode(motorPin8, OUTPUT);
  pinMode(motorPin9, OUTPUT);
  pinMode(motorPin10, OUTPUT);
  pinMode(motorPin11, OUTPUT);

  analogWrite(motorPin8, 0);
  analogWrite(motorPin9, 0);
  analogWrite(motorPin10, 0);
  analogWrite(motorPin11, 0);

  pinMode(switchPin20, INPUT);
  pinMode(switchPin21, INPUT);

  servo.attach(12); // GPIO12
}

void loop() {
  char key = 'f'; // シリアル通信の受信文字

  // シリアル通信の文字列チェック
  while(key != '0'){
    if ( Serial.available()){
      key = Serial.read();
    }
  }
  
  // 初期化
  wakeupMusic();

  
  moveFoward(150);

  Serial.print('9');

  while(1){

    // スイッチの状態を読み取る
    switchState20 = digitalRead(switchPin20);
    switchState21 = digitalRead(switchPin21);

    

    // スイッチが押されたとき
    if (switchState20 == LOW) {
      flag0 = flag0 + 1;
        if (flag0 == 1) {
          Serial.print('7');
        }

    }
    if (switchState21 == LOW) {
      flag1 = flag1 + 1;
      if (flag1 == 1) {
        Serial.print('8');
      }
    }
  
    if (switchState20 == HIGH) {
      flag0 = 0;
    }
    if (switchState21 == HIGH) {
      flag1 = 0;
    }

    if ( Serial.available()){
      key = Serial.read();
      if (key == '2'){
        shakingHead();

        while (key != '3'){
          if(Serial.available()){
            key = Serial.read();
          }
          shakingHead();
        }
      }
    }
  }

}
