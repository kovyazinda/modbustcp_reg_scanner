import sys
import time
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

if len(sys.argv) < 2:
    print("Error: No argument provided. Usage: python mb_scan_reg.py <ip-address>")
    sys.exit(1)

# Configuration
host = sys.argv[1]
port = 502
slave_id = 1
start_addr = 0
end_addr = 1000
logfile = host+'_modbus_scan_log.txt'
delay = 0.1


client = ModbusTcpClient(host, port)
client.connect()

with open(logfile, 'w') as log:
    for addr in range(start_addr, end_addr + 1):
        try:
            response = client.read_holding_registers(addr, 1, slave=slave_id)
            time.sleep(delay)
            if response.isError():
                log.write(f"Address {addr}: ERROR\n")
            else:
                value = response.registers[0]
                log.write(f"Address {addr}: Value = {value}\n")
        except ModbusException as e:
            log.write(f"Address {addr}: EXCEPTION - {str(e)}\n")

client.close()
print("Scan complete. Results in ", logfile)