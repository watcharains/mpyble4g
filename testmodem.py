#from sim7600 import SIM7600
from sim7600 import ascom
#import machine, time
from machine import Pin
import machine, time
import uasyncio as asyncio
import aswitch

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
#uart = machine.UART(1, baudrate=115200, tx=17, rx=18)
sim7600 = SIM_UART(uart_id=1, baudrate=115200, tx_pin=18, rx_pin=17)
#sim7600 = SIM7600(uart_id=1, baudrate=115200, tx_pin=18, rx_pin=17)
##volt = sim7600.monitor_voltage()
##print(volt)


async def test():
    res = await sim_uart.send_command('AT')
    if res:
        print('Result is:' , res)
    else:
        print('Timed out waiting for result.')

loop = asyncio.get_event_loop()
sim_uart = SIM_UART()
loop.run_until_complete(test())
