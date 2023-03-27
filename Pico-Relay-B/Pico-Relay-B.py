#  RP4020 Relais board SCPI interface
#  See https://www.waveshare.com/wiki/Pico-Relay-B#Download_Firmware

from machine import Pin
import time, rp2

class relaisBoard():
    def __init__(self, channels=8):
        self.channels = channels
        
        # Pin Assosiation for Waveshare Relais Board
        self.relais = {}
        self.relais[1] = {'state': 0, 'pin': 21, 'relais': None}
        self.relais[2] = {'state': 0, 'pin': 20, 'relais': None}
        self.relais[3] = {'state': 0, 'pin': 19, 'relais': None}
        self.relais[4] = {'state': 0, 'pin': 18, 'relais': None}
        self.relais[5] = {'state': 0, 'pin': 17, 'relais': None}
        self.relais[6] = {'state': 0, 'pin': 16, 'relais': None}
        self.relais[7] = {'state': 0, 'pin': 15, 'relais': None}
        self.relais[8] = {'state': 0, 'pin': 14, 'relais': None}
        
        for i in range(1,channels+1):
            self.relais[i]['relais'] = Pin(self.relais[i]['pin'],Pin.OUT)
        
        #  Initialise RGB LED
        self.rgb = Pin(13, Pin.OUT) #  RGB Led on Relais board
        self.led = Pin(25, Pin.OUT) #  On RP Pico
        
        #  Initialise Buzzer
        self.buzzer = Pin(6, Pin.OUT)
        
    def reset(self):
        for i in self.relais.keys():
            self.setRelais(channel=i, state='OFF')
        
    def read(self):
        readbuff = self.uart.readline()
        self.parseSCPI(msg=str(readbuff))
        
    def write(self, msg):
        uart.write('{}\n'.format(msg))
        
    def parseSCPI(self, msg):
        message = msg.split(':')
        
        #  Basic SCPI Commands:
        #  --------------------------------------------------------------------------------
        if len(message) == 1:
            if msg[0:5] == '*IDN?':
                print('Waveshare, RP4020 8 Channel Pico-Relay-B')
                
            elif msg[0:4] == '*RST':
                self.reset()
        
        #  Relais Subsystem Commands:
        #  --------------------------------------------------------------------------------
        elif len(message) == 3:
            system, channel, action = message
            system = system[0:4]
            
            if system == 'RELA':
                if action[0:4] == 'STAT' and action[-1] == '?':
                    try:
                        self.getRelais(channel=int(channel[-1]))
                    except Exception:
                        self.getRelais(channel=channel[-3::])
                    
                elif action[0:4] == 'STAT':
                    state = action.split(' ')[-1]
                    try:
                        self.setRelais(channel=int(channel[-1]), state=state)
                    except Exception:
                        self.setRelais(channel=int(channel[-1]), state=state)
                else:
                    print('Invalid Action -> [STATe?, STATe]')
            else:
                print('Invalid Subsystem -> [RELAis]')
        else:
            print('Invalid Command Format -> Relais:Channel<X>:State <0, OFF, 1, ON>')
    
    def setRelais(self, channel, state):
        if 'OFF' in state or state == '0':
            self.relais[channel]['state'] = 0
            self.relais[channel]['relais'].low()
            
        elif 'ON' in state or state == '1':
            self.relais[channel]['state'] = 1
            self.relais[channel]['relais'].high()
            
        else:
            print('Invalid State -> [0, OFF, 1, ON]')
    
    def getRelais(self, channel):
        if channel == 'ALL':
            status = []
            
            for i in range(1,self.channels+1):
                status.append('CH{}:{}'.format(i, self.relais[i]['state']))
            
            print(', '.join(status))
            
        elif 1 <= channel <= self.channels:
            print('CH{}:{}'.format(channel, self.relais[channel]['state']))
            
        else:
            print('Invalid channel [1-{}]'.format(self.channels))
            
    
if __name__=='__main__':
    relais = relaisBoard(channels=8)
    
    while True:
        try:
            test = input().replace('\\n','')
            relais.parseSCPI(msg=test)
        except Exception as e:
            print(e)
            raise(e)

    
        