import sys
import msvcrt
import serial, time
import paho.mqtt.client as mqtt
import json

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
MQTT_TOPIC_Monitor    = "MakerBase/user00/AttendInfo"


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_TOPIC_Monitor)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if (msg.topic == MQTT_TOPIC_Monitor):
        # 處理 JSON
        x = json.loads(msg.payload)
        # print(x)
        print(x["tag"], x["ename"], x["cname"])

        mp = x["ename"]
        print("TOPIC: [" + msg.topic + "], MESSAGE: " + mp + "]")

        ser.flushInput() #flush input buffer
        ser.flushOutput() #flush output buffer        
        ser.write(str.encode(mp))

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


# 等待使用者退出
print("\n按下 [Esc]鍵 可結束程式 !\n", ) 
 
while True:
    #client.loop()      # 無需執行 等待式檢查，已由 loop_async() 非同步模式 取代。
    if msvcrt.kbhit():  # Key Pressed
        if msvcrt.getch() == b'\x1b':  # [Esc] Key
            break
    time.sleep(MQTT_LOOP_Interval)

# 結束程式
client.loop_stop()
client.disconnect()
