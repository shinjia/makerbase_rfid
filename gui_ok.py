# UART Tx/Rx demo
import tkinter as tk
from tkinter import ttk
import serial
import threading
from datetime import datetime

class GUI:
    def __init__(self):
        window = tk.Tk()
        window.title("GUI UART Tx/Rx Demo")
        self.uartState = False # is uart open or not

        # a frame contains COM's information, and start/stop button
        frame_COMinf = tk.Frame(window)
        frame_COMinf.grid(row = 1, column = 1)

        labelCOM = tk.Label(frame_COMinf,text="COMx: ")
        self.COM = tk.StringVar(value = "COM5")
        ertryCOM = tk.Entry(frame_COMinf, textvariable = self.COM)
        labelCOM.grid(row = 1, column = 1, padx = 5, pady = 3)
        ertryCOM.grid(row = 1, column = 2, padx = 5, pady = 3)

        labelBaudrate = tk.Label(frame_COMinf,text="Baudrate: ")
        self.Baudrate = tk.IntVar(value = 115200)
        ertryBaudrate = tk.Entry(frame_COMinf, textvariable = self.Baudrate)
        labelBaudrate.grid(row = 1, column = 3, padx = 5, pady = 3)
        ertryBaudrate.grid(row = 1, column = 4, padx = 5, pady = 3)

        labelParity = tk.Label(frame_COMinf,text="Parity: ")
        self.Parity = tk.StringVar(value ="NONE")
        comboParity = ttk.Combobox(frame_COMinf, width = 17, textvariable=self.Parity)
        comboParity["values"] = ("NONE","ODD","EVEN","MARK","SPACE")
        comboParity["state"] = "readonly"
        labelParity.grid(row = 2, column = 1, padx = 5, pady = 3)
        comboParity.grid(row = 2, column = 2, padx = 5, pady = 3)

        labelStopbits = tk.Label(frame_COMinf,text="Stopbits: ")
        self.Stopbits = tk.StringVar(value ="1")
        comboStopbits = ttk.Combobox(frame_COMinf, width = 17, textvariable=self.Stopbits)
        comboStopbits["values"] = ("1","1.5","2")
        comboStopbits["state"] = "readonly"
        labelStopbits.grid(row = 2, column = 3, padx = 5, pady = 3)
        comboStopbits.grid(row = 2, column = 4, padx = 5, pady = 3)
        
        self.buttonSS = tk.Button(frame_COMinf, text = "Start", command = self.processButtonSS)
        self.buttonSS.grid(row = 3, column = 4, padx = 5, pady = 3, sticky = tk.E)

        # serial object
        self.ser = serial.Serial()
        # serial read threading
        self.ReadUARTThread = threading.Thread(target=self.ReadUART)
        self.ReadUARTThread.start()

        frameRecv = tk.Frame(window)
        frameRecv.grid(row = 2, column = 1)
        labelOutText = tk.Label(frameRecv,text="Received Data:")
        labelOutText.grid(row = 1, column = 1, padx = 3, pady = 2, sticky = tk.W)
        frameRecvSon = tk.Frame(frameRecv)
        frameRecvSon.grid(row = 2, column =1)
        scrollbarRecv = tk.Scrollbar(frameRecvSon)
        scrollbarRecv.pack(side = tk.RIGHT, fill = tk.Y)
        self.OutputText = tk.Text(frameRecvSon, wrap = tk.WORD, width = 60, height = 20, yscrollcommand = scrollbarRecv.set)
        self.OutputText.pack()

        frameTrans = tk.Frame(window)
        frameTrans.grid(row = 3, column = 1)
        labelInText = tk.Label(frameTrans,text="To Transmit Data:")
        labelInText.grid(row = 1, column = 1, padx = 3, pady = 2, sticky = tk.W)
        frameTransSon = tk.Frame(frameTrans)
        frameTransSon.grid(row = 2, column =1)
        scrollbarTrans = tk.Scrollbar(frameTransSon)
        scrollbarTrans.pack(side = tk.RIGHT, fill = tk.Y)
        self.InputText = tk.Text(frameTransSon, wrap = tk.WORD, width = 60, height = 5, yscrollcommand = scrollbarTrans.set)
        self.InputText.pack()
        self.buttonSend = tk.Button(frameTrans, text = "Send", command = self.processButtonSend)
        self.buttonSend.grid(row = 3, column = 1, padx = 5, pady = 3, sticky = tk.E)
        
        window.mainloop()

    def processButtonSS(self):
        # print(self.Parity.get())
        if (self.uartState):
            self.ser.close()
            self.buttonSS["text"] = "Start"
            self.uartState = False
        else:
            # restart serial port
            self.ser.port = self.COM.get()
            self.ser.baudrate = self.Baudrate.get()
            
            strParity = self.Parity.get()
            if (strParity=="NONE"):
                self.ser.parity = serial.PARITY_NONE;
            elif(strParity=="ODD"):
                self.ser.parity = serial.PARITY_ODD;
            elif(strParity=="EVEN"):
                self.ser.parity = serial.PARITY_EVEN;
            elif(strParity=="MARK"):
                self.ser.parity = serial.PARITY_MARK;
            elif(strParity=="SPACE"):
                self.ser.parity = serial.PARITY_SPACE;
                
            strStopbits = self.Stopbits.get()
            if (strStopbits == "1"):
                self.ser.stopbits = serial.STOPBITS_ONE;
            elif (strStopbits == "1.5"):
                self.ser.stopbits = serial.STOPBITS_ONE_POINT_FIVE;
            elif (strStopbits == "2"):
                self.ser.stopbits = serial.STOPBITS_TWO;
            
            self.ser.open()
            if (self.ser.isOpen()): # open success
                self.buttonSS["text"] = "Stop"
                self.uartState = True

    def processButtonSend(self):
        if (self.uartState):
            strToSend = self.InputText.get(1.0,tk.END)
            bytesToSend = strToSend[0:-1].encode(encoding='ascii')
            self.ser.write(bytesToSend)
            print(bytesToSend)
        else:
            print("Not In Connect!")

    def ReadUART(self):
        # print("Threading...")
        while True:
            if (self.uartState):
                try:
                    # Part1: 得到 RFID 的 Tag
                    data_str = self.ser.readline().decode(encoding='ascii')
                    rfid_code = data_str.strip()

                    # Part2: 比對內容
                    msg = "(x)"
                    if rfid_code in dict:
                        msg = dict[rfid_code]

                    # Part3: 回傳結果            
                    self.ser.write(str.encode(msg))
                    msg_show = datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + ", "
                    msg_show += rfid_code + ", "
                    msg_show += msg

                    print(msg_show)
                    
                    self.OutputText.insert(tk.END,msg_show+"\n")
                except:
                    print("Something wrong in receiving.")


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

GUI()
