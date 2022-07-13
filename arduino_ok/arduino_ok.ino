#include <SPI.h> 

#include <MFRC522.h>
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

#include "pitches.h"

#define SS_PIN 10 
#define RST_PIN 9 

#define BEEP_PIN 8

LiquidCrystal_I2C lcd(0x27, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);
MFRC522 mfrc522(SS_PIN, RST_PIN); // Instance of the class


struct RFIDTag {   // 定義結構
   String code;
   String name;
};

// stored records. code must be UpperCase
struct RFIDTag tags[] = {
  {"96ABC1F7", "Wayne"},
  {"7340341C", "Shinjia"},
  {"C3223D1C", "Admin"}
};

byte totalTags = sizeof(tags) / sizeof(RFIDTag);  // 計算結構資料筆數，結果為3。

// for LCD
String str1_welcome = "RFID Card Reader";
String str2_welcome = "----------------";
String str1, str2;

// for timer control
int timer_interval_clear = 5000;  // 多久時間候清除畫面
unsigned long timer_next_clear;

boolean is_debug = false;


void beep(int type=0)
{
  // notes in the melody:
  int melody[] = {
    NOTE_C4, NOTE_G3, NOTE_G3, NOTE_A3, NOTE_G3, 0, NOTE_B3, NOTE_C4
  };
  
  // note durations: 4 = quarter note, 8 = eighth note, etc.:
  int noteDurations[] = {
    4, 8, 8, 4, 4, 4, 4, 4
  };

  switch(type)
  {
    case 0:  // 起始音效
      for (int thisNote=0; thisNote<8; thisNote++)
      {
        int noteDuration = 1000 / noteDurations[thisNote];
        tone(8, melody[thisNote], noteDuration);
    
        int pauseBetweenNotes = noteDuration * 1.30;
        delay(pauseBetweenNotes);
        // stop the tone playing:
        noTone(8);
      }
      break;
      
    case 1:  // 可通行卡片的音效
      tone(8, NOTE_A4, 1000/8); delay(200); noTone(8);
      tone(8, NOTE_B4, 1000/8); delay(200); noTone(8);
      break;
      
    case 2:  // 不可通行卡片的音效
      tone(8, NOTE_C4, 1000/8); delay(200); noTone(8);
      tone(8, NOTE_G4, 1000/4); delay(200); noTone(8);
      tone(8, NOTE_C4, 1000/8); delay(200); noTone(8);
      tone(8, NOTE_G4, 1000/4); delay(200); noTone(8);
      break;
  }
}


void lcd_display(String str1, String str2)
{
  String str0 = "                ";  // 16個空白
 
  // Print a message to the LCD. 
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print(str1+str0);
  lcd.setCursor(0,1);
  lcd.print(str2+str0);
}

void setup()
{
  Serial.begin(115200);
  if(is_debug)
  {
    Serial.println("Arduino RFID reading UID");
  }

  // RFID
  SPI.begin();       // Init SPI bus
  mfrc522.PCD_Init(); // Init MFRC522 

  // LCD 顯示
  lcd.begin(16,2);
  //lcd.init();
  lcd.backlight();
  lcd_display(str1_welcome, str2_welcome);

  // Buzzle 聲音
  pinMode(BEEP_PIN, OUTPUT);
  beep(0);

  // 時間控制
  timer_next_clear = millis() + timer_interval_clear;
}


void loop()
{
  String rfid_code = "";
  String rfid_name = "";

  if (mfrc522.PICC_IsNewCardPresent())
  {
    if ( mfrc522.PICC_ReadCardSerial())
    {
      for (byte i=0; i<mfrc522.uid.size; i++)
      {
        rfid_code += mfrc522.uid.uidByte[i] < 0x10 ? "0" : "";
        rfid_code += String(mfrc522.uid.uidByte[i], HEX);
        rfid_code.toUpperCase();        
      }

      // check code
      boolean match = false;
      
      for (int i=0; i<totalTags; i++)
      {
        if(rfid_code==tags[i].code)
        {
          match = true;
          rfid_name = tags[i].name;
          break;
        }
      }

      Serial.println(rfid_code);
      
      if(match)
      {
        if(is_debug)
        {
          Serial.println("Valid Card --- ");
          Serial.println(rfid_name);
        }

        str1 = "code: " + rfid_code;
        str2 = "name: " + rfid_name;
        lcd_display(str1, str2);
        beep(1);
      }
      else
      {
        if(is_debug)
        {
          Serial.println("Unknown Card");
        }
              
        str1 = "code: " + rfid_code;
        str2 = "name: (X)reject";
        lcd_display(str1, str2);
        beep(2);
      }

      // Serial.println("============================");
      mfrc522.PICC_HaltA();

      timer_next_clear = millis() + timer_interval_clear;
    }
  }
  
  // serial read
  if(Serial.available())
  {
    while(Serial.available() > 0)
    {
      // lcd.write(Serial.read());
      str1 = "from serial port";
      str2 = Serial.readString();
      lcd_display(str1, str2);
    }
    
    timer_next_clear = millis() + timer_interval_clear;
  }

  if(millis()>timer_next_clear)
  {
    timer_next_clear = millis() + timer_interval_clear;
    lcd_display(str1_welcome, str2_welcome);
  }
}
