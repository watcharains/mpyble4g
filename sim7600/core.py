import machine
import time

class SIM7600:
    def __init__(self, uart_id, tx_pin, rx_pin, baudrate=115200):
        self.uart = machine.UART(uart_id, baudrate=baudrate, tx=tx_pin, rx=rx_pin)

    def send_command(self, command, timeout=3000):
        command += '\r\n'
        self.uart.write(command)
        start_time = time.ticks_ms()
        response = []
        while time.ticks_diff(time.ticks_ms(), start_time) < timeout:
            if self.uart.any():
                response.append(self.uart.read().decode())
        return ''.join(response)

    def power_on(self):
        return self.send_command('AT+CFUN=1')

    def power_off(self):
        return self.send_command('AT+CPOF')

    def reset_module(self):
        return self.send_command('AT+CRESET')

    def set_power_mode(self, mode):
        return self.send_command(f'AT+CSCLK={mode}')

    def monitor_voltage(self):
        return self.send_command('AT+CBC')

    def connect(self, apn, user='', password=''):
        self.send_command('AT+CGATT=1')
        self.send_command(f'AT+CSTT="{apn}","{user}","{password}"')
        self.send_command('AT+CIICR')
        return self.send_command('AT+CIFSR')

    def disconnect(self):
        return self.send_command('AT+CGATT=0')

    def get_network_status(self):
        return self.send_command('AT+CREG?')

    def set_flight_mode(self, enable):
        return self.send_command(f'AT+CFUN={0 if enable else 1}')
    def at_checking(self):
        return self.send_command('AT')
    def get_gsm_location(self):
        """
        Get the GSM location based on the nearest cell tower.
        Returns the longitude and latitude along with a timestamp.
        """
        response = self.send_command('AT+CIPGSMLOC=1,1')
        return response
#Network
    def chksimcard(self):#ReT OK
        return self.send_command('AT+CPIN?') 
    def chksignal(self):#ReT OK
        return self.send_command('AT+CSQ') 
    def chkcsservice(self):#ReT OK
        return self.send_command('AT+CREG?')
    def chkpsservice1(self):#ReT OK
        return self.send_command('AT+CGREG?')
    def chkpsservice2(self):#ReT OK
        return self.send_command('AT+CEREG?')
    def chkueinfo(self):#ReT OK
        return self.send_command('AT+CPSI?')
    
    def configpdp(self):#ReT OK
        return self.send_command('AT+CGDCONT= 1,"IP","internet","0.0.0.0",0,0')
    def activepdp(self):#ReT OK
        return self.send_command('AT+CGACT=1,1')
    def chkpdp(self):#ReT OK
        return self.send_command('AT+CGACT?')    
#MQTT
    def openmqttservice(self):#ReT OK
        return self.send_command('AT+CMQTTSTART')
    def applymqttclient(self):
        return self.send_command('AT+CMQTTACCQ=0,"BleXtreme001",0')    
    def sendmqttconnect(self):
        return self.send_command('AT+CMQTTCONNECT=0,"tcp://61.91.50.18:1884",20,1,"tobb","tb9918t"')     
    def startinputpubtopic(self):
        self.send_command('AT+CMQTTTOPIC=0,8')
        return self.send_command('BX001PUB')
    def sendpayload(self,json_string):
        payloadstring = str(json_string)
        length_in_bytes = len(payloadstring)
        cmdstring='AT+CMQTTPAYLOAD=0,'+str(length_in_bytes)
        print(cmdstring)
        self.send_command(cmdstring)
        return self.send_command(payloadstring)
    def pubtopic(self):
        return self.send_command('AT+CMQTTPUB=0,1,60')
    
    