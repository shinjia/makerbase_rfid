import serial, time

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

while(True):
    if(ser.inWaiting()>0):
        # Part1: 得到 RFID 的 Tag
        data_str = ser.read(ser.inWaiting()).decode('ascii') 
        rfid_code = data_str.strip()

        # Part2: 比對內容
        msg = "(x)"
        if rfid_code in dict:
            msg = dict[rfid_code]

        # Part3: 回傳結果            
        ser.write(str.encode(msg))
        print(rfid_code + "," + msg)

    time.sleep(0.01)

