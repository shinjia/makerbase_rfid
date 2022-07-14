float prob = 0.7;  // 出現正確刷卡的機率

struct RFIDTag {   // 定義結構
   String code;
   String name;
};

// stored records. code must be UpperCase
struct RFIDTag tags[] = {
  {"96ABC1F7", "Wayne"},
  {"7340341C", "Shinjia"},
  {"B76E3685", "Bruce"},
  {"C1234567", "Candy"},
  {"D4F514C5", "David"},
  {"C3223D1C", "Admin"}
};

byte totalTags = sizeof(tags) / sizeof(RFIDTag);  // 計算結構資料筆數，結果為3。

// for timer control
unsigned long timer_next;  // 多久時間產生下一個
int timer_min =  5000;
int timer_max = 10000;

boolean is_debug = false;


void led(int type)
{
  switch(type)
  {
    case 0: // always dark
       digitalWrite(LED_BUILTIN, 0);
       break;
       
    case 1: // valid
       for(int i=0; i<3; i++)
       {
         digitalWrite(LED_BUILTIN, 1); delay(300);
         digitalWrite(LED_BUILTIN, 0); delay(300);
       }
       break;
       
    case 2: // invalid
       for(int i=0; i<8; i++)
       {
         digitalWrite(LED_BUILTIN, 1); delay(100);
         digitalWrite(LED_BUILTIN, 0); delay(100);
       }
       break;
       
    case 3: // just blink
       digitalWrite(LED_BUILTIN, 1); delay(100);
       digitalWrite(LED_BUILTIN, 0); delay(100);
       break;
       
    case 9: // always high
       digitalWrite(LED_BUILTIN, 1);
       break;
  }
}

void setup()
{
  Serial.begin(115200);
  if(is_debug)
  {
    Serial.println("Simulate RFID reading UID");
  }

  // LED
  pinMode(LED_BUILTIN, OUTPUT);

  // 時間控制
  timer_next = millis() + random(timer_min, timer_max);
}


void loop()
{
  String rfid_code, rfid_name;
  int idx;
  if(millis()>timer_next)
  {
    if((float)random(0, 10)/10 < prob)
    {
      // 出現正確刷卡
      idx = random(totalTags);
      rfid_code = tags[idx].code;
      rfid_name = tags[idx].name;
      led(1);
    }
    else
    {
      rfid_code = "";
      rfid_name = "Unknown";
      for (byte i=0; i<4; i++)
      {
        byte choice = random(0, 255);
        rfid_code += choice < 0x10 ? "0" : "";
        rfid_code += String(choice, HEX);
        rfid_code.toUpperCase();        
      }
      led(2);
    }
  
    Serial.println(rfid_code);
    if(is_debug)
    {
      Serial.println(rfid_name);
    }
    timer_next = millis() + random(timer_min, timer_max);
  }
  
  // serial read
  if(Serial.available())
  {
    while(Serial.available() > 0)
    {
      rfid_code = Serial.readString();
      if(is_debug)
      {
        Serial.print("From Serial port---> ");
        Serial.println(rfid_code);
      }
      for(int i=0; i<rfid_code.length(); i++)
      {
        led(3);
      }
    }
    
    timer_next = millis() + random(timer_min, timer_max);
  }
}
