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

while(True):
    if ser.isOpen():
        try:
            msg = input("Input string:")
            
            ser.flushInput() #flush input buffer
            ser.flushOutput() #flush output buffer
            
            ser.write(str.encode(msg))
            print(msg)
            
            time.sleep(0.5)  #wait 0.5s

        except Exception as e1:
            print ("communicating error " + str(e1))

    else:
        print ("open serial port error")
