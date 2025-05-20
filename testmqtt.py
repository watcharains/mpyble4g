from sim7600 import SIM7600
from machine import Pin
import machine, time
import random
import json
# Function to generate random MAC address (for simulation)
def generate_mac_address():
    return "AA:BB:CC:{:02X}:{:02X}:{:02X}".format(
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )

# Function to generate simulated Bluetooth device data
def generate_bluetooth_data():
    num_devices = random.randint(0, 5)  # Simulate 0-5 devices found
    devices = []
    for _ in range(num_devices):
        device = {
            "mac": generate_mac_address(),
            "rssi": random.randint(-90, -30),  # Realistic RSSI range
        }
        devices.append(device)
    return devices
# Function to generate simulated sensor data
def generate_sensor_data():
    voltage = round(random.uniform(3.6, 4.2), 2)  # Typical Li-ion voltage
    network_status = "connected" if random.random() > 0.1 else "disconnected"  # Simulate occasional disconnects
    return voltage, network_status


#p45 = Pin(45, Pin.OUT)    # create output pin on GPIO0
#p45.on()                 # set pin to "on" (high) level
#p45.off()                # set pin to "off" (low) level
#p45.value(1)             # set pin to on/high

#p40 = Pin(40, Pin.OUT)    # create output pin on GPIO0
#p40.on()                 # set pin to "on" (high) level
#p40.off()                # set pin to "off" (low) level
#p40.value(1)             # set pin to on/high

##print("Init")
#time.sleep(5)
# Initialize the SIM7600 module
sim7600 = SIM7600(uart_id=1, baudrate=115200, tx_pin=18, rx_pin=17)
volt = sim7600.get_network_status()
print(volt)

ret = sim7600.chksimcard()
print(ret)
ret = sim7600.chksignal()
print(ret)
ret = sim7600.chkcsservice()
print(ret)
ret = sim7600.chkpsservice1()
print(ret)
ret = sim7600.chkpsservice2()
print(ret)
ret = sim7600.chkueinfo()
print(ret)

ret = sim7600.configpdp()
print(ret)
ret = sim7600.activepdp()
print(ret)
ret = sim7600.chkpdp()
print(ret)

ret = sim7600.openmqttservice()
print(ret)
ret = sim7600.applymqttclient()
print(ret)
ret = sim7600.sendmqttconnect()
print(ret)
#now Pub Topic
roundcount=0
while True:
    roundcount=roundcount+1
    ret = sim7600.startinputpubtopic()
    print(ret)
    #init Payload
    
    #DATA FROM GEN
    voltage, network_status = generate_sensor_data() #remove voltage and network status
    bluetooth_devices = generate_bluetooth_data()
    current_time = roundcount

        # Construct the JSON payload
    payloadstr = {
            "voltage": voltage, #remove voltage
            "network_status": network_status, #remove network status
            "time": current_time,
            "num_devices": len(bluetooth_devices),
            "devices": bluetooth_devices,
    }
    json_payload = json.dumps(payloadstr)
    print(json_payload)
    ret = sim7600.sendpayload(payloadstr)
    print(ret)
    ret = sim7600.pubtopic()
    print(ret)
    time.sleep(3)


