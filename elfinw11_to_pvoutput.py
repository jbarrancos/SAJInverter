from pymodbus.client.sync import ModbusTcpClient
import time
import requests
from datetime import datetime

host = 'xx.xx.xx.xx' 
port = 8899

client = ModbusTcpClient(host, port)
client.connect()

while 1:

    try:
            # retrieving all 41 in one go
            rr = client.read_holding_registers(0x0104,41,unit=1)
            assert(rr.function_code < 0x80)

            Realtime_ACW_1 = rr.registers[5] # 0x0109
            Realtime_ACW_2 = rr.registers[8] # 0x010C
            print("AC_Watts 1: " + str(Realtime_ACW_1) + "W")
            print("AC_Watts 2: " + str(Realtime_ACW_2) + "W")
            Realtime_DCV_1 = rr.registers[3] # 0x0107
            Realtime_DCV_2 = rr.registers[6] # 0x010A
            print("DC Volt 1: " + str(Realtime_DCV_1) + "V")
            print("DC Volt 2: " + str(Realtime_DCV_2) + "V")
            Realtime_DCI = rr.registers[4] # 0x0108
            Realtime_DCI = rr.registers[7] # 0x010B
            print("DC Current : " + str(Realtime_DCI) + "A")
            print("DC Current : " + str(Realtime_DCI) + "A")

            Realtime_LW1 = rr.registers[22] # 0x011A
            print("L1 AC Watt: " + str(Realtime_LW1) + "W")
            Realtime_LW2 = rr.registers[28] #0x0120
            print("L2 AC Watt: " + str(Realtime_LW2) + "W")

            Realtime_ACV = rr.registers[19] #0x0116
            print("L1 AC volt : " + str(Realtime_ACV) + "V")
            Realtime_ACI = rr.registers[19] #0x0117
            print("L1 AC Current :" + str(Realtime_ACI) + "A")
            Realtime_ACF = rr.registers[20] #0x0118
            print("L1 AC Frequency :"+ str(Realtime_ACF) + "Hz")
            Realtime_ACV2 = rr.registers[24] #0x011C
            print("L2 AC volt : " + str(Realtime_ACV2) + "V")
            Realtime_ACI2 = rr.registers[25] #0x011D
            print("L2 AC Current :" + str(Realtime_ACI2) + "A")
            Realtime_ACF2 = rr.registers[26] #0x011E
            print("L2 AC Frequency :"+ str(Realtime_ACF2) + "Hz")
            Inverter_C = rr.registers[13] #0x0111
            print("Inverter Temperature :" + str(Inverter_C) + "C")
            Today_KW = rr.registers[40] #0x012C 
            print("Generated (Today) :" + str(Today_KW) + "kW")
            today = datetime.now()

            url = 'https://pvoutput.org/service/r2/addstatus.jsp'
            headers = { 'X-Pvoutput-Apikey' : 'your-api-key', 'X-Pvoutput-SystemId': 'your-system-id' }
            pvoutput = {'d': today.strftime("%Y%m%d"), 't': today.strftime('%H:%M'),'v2': str(Realtime_ACW_1+Realtime_ACW_2), 'v6': str((Realtime_DCV_1+Realtime_DCV_2)/2)}

            print (pvoutput)
            x = requests.post(url, data = pvoutput, headers = headers)
            print(x.text)


    except Exception as e:
            print("Exception: ", str(e));
            print("Reconnecting.")
            client.close()
            client = ModbusTcpClient(host, port)
            client.connect()
    
    print ("Sleep for 5 minutes")
    # Sleep 5 minutes
    time.sleep(300)
