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
MQTT_TOPIC_Monitor    = "MakerBase/user00/TagID"

# MQTT 連線準備
client = mqtt.Client()
#client.username_pw_set(username=MQTT_USER, password=MQTT_PWD)  # 若無需使用者帳密，則直接刪除本行！
client.connect(MQTT_SERVER, 1883, 60)
 
try: 
    ser.open()
except Exception as ex:
    print ("open serial port error " + str(ex))
    exit()

while(True):
    if(ser.inWaiting()>0):
        # read the bytes and convert from binary array to ASCII
        data_str = ser.read(ser.inWaiting()).decode('ascii') 
        # print the incoming string without putting a new-line
        # ('\n') automatically after every print()
        print(data_str, end='') 
        
        # 發送 mqtt
        info = client.publish(MQTT_TOPIC_Monitor, data_str)

    time.sleep(0.01)

# 結束程式
client.disconnect()