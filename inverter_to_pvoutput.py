import minimalmodbus
import socket
import serial
import time
import requests
from datetime import datetime

#
# Script can be scheduled every 5 minutes for PVOutput reporting
#

instrument = minimalmodbus.Instrument('/dev/serial0', 1)
instrument.serial.baudrate = 9600
instrument.serial.bytesize = 8
instrument.serial.parity   = serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout  = 0.2

try:

        Realtime_ACW_1 = instrument.read_register(0x0109, number_of_decimals=0, functioncode=3, signed=False)
        Realtime_ACW_2 = instrument.read_register(0x010C, number_of_decimals=0, functioncode=3, signed=False)
        print("AC_Watts 1: " + str(Realtime_ACW_1) + "W")
        print("AC_Watts 2: " + str(Realtime_ACW_2) + "W")
        Realtime_DCV_1 = instrument.read_register(0x0107, number_of_decimals=1, functioncode=3, signed=False)
        Realtime_DCV_2 = instrument.read_register(0x010A, number_of_decimals=1, functioncode=3, signed=False)
        print("DC Volt 1: " + str(Realtime_DCV_1) + "V")
        print("DC Volt 2: " + str(Realtime_DCV_2) + "V")
        Realtime_DCI = instrument.read_register(0x0108, number_of_decimals=2, functioncode=3, signed=False)
        Realtime_DCI = instrument.read_register(0x010B, number_of_decimals=2, functioncode=3, signed=False)
        print("DC Current : " + str(Realtime_DCI) + "A")
        print("DC Current : " + str(Realtime_DCI) + "A")

        Realtime_LW1 = instrument.read_register(0x011A, number_of_decimals=0, functioncode=3, signed=False)
        print("L1 AC Watt: " + str(Realtime_LW1) + "W")
        Realtime_LW2 = instrument.read_register(0x0120, number_of_decimals=0, functioncode=3, signed=False)
        print("L2 AC Watt: " + str(Realtime_LW2) + "W")

        Realtime_ACV = instrument.read_register(0x0116, number_of_decimals=1, functioncode=3, signed=False)
        print("L1 AC volt : " + str(Realtime_ACV) + "V")
        Realtime_ACI = instrument.read_register(0x0117, number_of_decimals=2, functioncode=3, signed=False)
        print("L1 AC Current :" + str(Realtime_ACI) + "A")
        Realtime_ACF = instrument.read_register(0x0118, number_of_decimals=2, functioncode=3, signed=False)
        print("L1 AC Frequency :"+ str(Realtime_ACF) + "Hz")
        Realtime_ACV2 = instrument.read_register(0x011C, number_of_decimals=1, functioncode=3, signed=False)
        print("L2 AC volt : " + str(Realtime_ACV2) + "V")
        Realtime_ACI2 = instrument.read_register(0x011D, number_of_decimals=2, functioncode=3, signed=False)
        print("L2 AC Current :" + str(Realtime_ACI2) + "A")
        Realtime_ACF2 = instrument.read_register(0x011E, number_of_decimals=2, functioncode=3, signed=False)
        print("L2 AC Frequency :"+ str(Realtime_ACF2) + "Hz")
        Inverter_C = instrument.read_register(0x0111, number_of_decimals=1, functioncode=3, signed=True)
        print("Inverter Temperature :" + str(Inverter_C) + "C")
        Today_KW = instrument.read_register(0x012C, number_of_decimals=2, functioncode=3, signed=False) 
        print("Generated (Today) :" + str(Today_KW) + "kW")
        today = datetime.now()

        url = 'https://pvoutput.org/service/r2/addstatus.jsp'
        headers = { 'X-Pvoutput-Apikey' : 'your-api-key', 'X-Pvoutput-SystemId': 'your-system-id' }
        pvoutput = {'d': today.strftime("%Y%m%d"), 't': today.strftime('%H:%M'),'v2': str(Realtime_ACW_1+Realtime_ACW_2), 'v6': str((Realtime_DCV_1+Realtime_DCV_2)/2)}

        print pvoutput
        x = requests.post(url, data = pvoutput, headers = headers)
        print(x.text)

except Exception, e:
        print(str(e));

