import sys
import msvcrt
import serial, time
import paho.mqtt.client as mqtt

# ser = serial.Serial(port="COM5", baudrate=115200)
ser = serial.Serial()
ser.port = "COM5"

#115200,N,8,1
ser.baudrate = 115200
ser.bytesize = serial.EIGHTBITS #number of bits per bytes
ser.parity = serial.PARITY_NONE #set parity check
ser.stopbits = serial.STOPBITS_ONE #number of stop bits

ser.timeout = 0.5          #non-block read 0.5s
ser.writeTimeout = 0.5     #timeout for write 0.5s
ser.xonxoff = False    #disable software flow control
ser.rtscts = False     #disable hardware (RTS/CTS) flow control
ser.dsrdtr = False     #disable hardware (DSR/DTR) flow control


# MQTT 參數設定
MQTT_SERVER           = "mqttgo.io"
#MQTT_USER             = "my_name"
#MQTT_PWD              = "my_password"
MQTT_LOOP_Interval    = 0.05                  
MQTT_TOPIC_Face       = "MakerBase/shinjia/FaceID"
MQTT_TOPIC_Tag        = "MakerBase/shinjia/TagID"


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_TOPIC_Face)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if (msg.topic == MQTT_TOPIC_Face):
        mp = msg.payload.decode('ascii')
        print("TagID ==> TOPIC: [" + msg.topic + "], MESSAGE: " + mp + "]")

        ser.flushInput() #flush input buffer
        ser.flushOutput() #flush output buffer
        ser.write(str.encode("@F"+mp))

    else: # other topics
        mp = msg.payload.decode('ascii')
        print("TOPIC: [" + msg.topic + "], MESSAGE: " + mp + "]")


# MQTT 連線準備
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
#client.username_pw_set(username=MQTT_USER, password=MQTT_PWD)  # 若無需使用者帳密，則直接刪除本行！
client.connect_async(MQTT_SERVER, 1883, 60)  #  連結 MQTT Server，指定以 非同步模式 執行 MQTT Message 傳入檢查。
client.loop_start()    

try: 
    ser.open()
except Exception as ex:
    print ("open serial port error " + str(ex))
    exit()


def getData():
    file = open('card.txt', 'r')
    data = file.readlines()
    myDic = {}
    for line in data:
        (code, name) = line.strip().split(',')
        myDic[code] = name
    file.close()
    return myDic

# Part0: 讀取資料檔案
dict = getData()
# print("Data type before reconstruction : ", type(dict))
print(dict)


# 等待使用者退出
print("\n按下 [Esc]鍵 可結束程式 !\n", ) 
 
while True:
    if(ser.inWaiting()>0):
        # Part1: 得到 RFID 的 Tag
        data_str = ser.read(ser.inWaiting()).decode('ascii') 
        rfid_code = data_str.strip()
        # 同時 Mqtt pub
        client.publish(MQTT_TOPIC_Tag, rfid_code)

        # Part2: 比對內容
        msg = "(x)"
        if rfid_code in dict:
            msg = dict[rfid_code]

        # Part3: 回傳結果            
        ser.write(str.encode("@T"+msg))
        print(rfid_code + "," + msg)

    #client.loop()      # 無需執行 等待式檢查，已由 loop_async() 非同步模式 取代。
    if msvcrt.kbhit():  # Key Pressed
        if msvcrt.getch() == b'\x1b':  # [Esc] Key
            break
    time.sleep(MQTT_LOOP_Interval)

# 結束程式
client.loop_stop()
client.disconnect()
