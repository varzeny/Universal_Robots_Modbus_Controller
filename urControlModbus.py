from pymodbus.client import ModbusTcpClient
from struct import *

# if (val > 32768): val = val - 65535

class UrModbusController:
    def __init__(self,ip):
        self.client=ModbusTcpClient(ip,502)

    def __del__(self):
        self.client.close()

    def func_transReadUr(self, n):
        return unpack('>h',pack('>H',n))[0]/1000

    def func_transSendUr(self, n):
        return unpack('>H',pack('>h',int(n*1000)))[0]

    def func_checkTCP(self,start_rg=400):
        return [self.func_transReadUr(n) for n in self.client.read_holding_registers(start_rg,6).registers]

    def func_moveTCP(self, tcp_goal, start_rg=200):
        for i in range(6):
            self.client.write_registers(start_rg+i, self.func_transSendUr(tcp_goal[i]))


if __name__=="__main__":
    robot=UrModbusController("192.168.1.104")
    robot.func_moveTCP([0.1,-0.3,0.2,0.0,-3.14,0.0])
    #robot.func_moveTCP([0.05,-0.05,0.05,0.0,0.0,0.0])
    print( robot.func_checkTCP() )