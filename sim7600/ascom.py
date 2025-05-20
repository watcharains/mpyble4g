import machine
import uasyncio as asyncio
import aswitch

class SIM_UART():
        def __init__(self, uart_id, tx_pin, rx_pin, baudrate=115200):
        self.uart = machine.UART(uart_id, baudrate=baudrate, tx=tx_pin, rx=rx_pin)
        self.timeout = 4000
        self.loop = asyncio.get_event_loop()
        self.swriter = asyncio.StreamWriter(self.uart, {})
        self.sreader = asyncio.StreamReader(self.uart)
        self.delay = aswitch.Delay_ms()
        self.response = []
        loop = asyncio.get_event_loop()
        loop.create_task(self.recv())

    async def recv(self):
        while True:
            res = await self.sreader.readline()
            self.response.append(res)  # Append to list of lines
            self.delay.trigger(self.timeout)  # Got something, retrigger timer

    async def send_command(self, command):
        self.response = []  # Discard any pending messages
        await self.swriter.awrite("{}\r\n".format(command))
        print("<", command)
        self.delay.trigger(self.timeout)  # Re-initialise timer
        while self.delay.running():
            await asyncio.sleep(1)  # Wait for 4s after last msg received
        return b''.join(self.response)

