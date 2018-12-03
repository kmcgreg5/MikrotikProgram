import subprocess
import re
import time
def getPanelList(): #gets ips and MAC addresses of ips in the 192.168.88.## or 192.168.87.## format
    CREATE_NO_WINDOW = 0x08000000
    cmdCommand = subprocess.Popen(['arp','-a'], stdout = subprocess.PIPE, creationflags = CREATE_NO_WINDOW)
    arpReturn = cmdCommand.communicate()
    arpReturn = str(arpReturn[0])
    numIPs = arpReturn.count('192.168.88')
    numIPs = numIPs + arpReturn.count('192.168.87')
    numInterfaces = arpReturn.count('Interface')
    numIPs = numIPs - numInterfaces + 1
    interfaceList = ['None' for x in range(numInterfaces)]
    x = 0
    index2 = 0
    while x < numInterfaces: #populates interface list
        interfaceIndex = arpReturn.index('Interface', index2)
        interfaceList[x] = arpReturn[interfaceIndex + 11: interfaceIndex + 11 + 13]
        interfaceList[x] = interfaceList[x].strip()
        index2 = interfaceIndex + 5
        x += 1

    ipMACList = [['None' for x in range(2)] for y in range(numIPs)]
    print(len(ipMACList))
    x = 0
    index = 0
    index2 = 0
    done = False
    done2 = False
    while True: #populates ipMACList with IPs and MAC addresses of wanted panels
        try:
            ipIndex = arpReturn.index('192.168.88', index) #once for .88 ips
            index = ipIndex + 5
            ip = arpReturn[ipIndex: ipIndex + 13]
            ip = ip.strip()
            testValidity = re.match('192\.168\.88\.\d{1,2}', ip) #regex for accepted IPs
            testInterface = True
            for y in interfaceList:
                if ip == y:
                    testInterface = False
            
            if testValidity is not None and testInterface:
                ipMACList[x][0] = ip
                ipMACList[x][1] = arpReturn[ipIndex + 13 + 9:ipIndex + 13 + 9 + 17]
                x += 1
        except ValueError:
            done = True
            
        try:
            ipIndex2 = arpReturn.index('192.168.87', index2) #once for .87 ips
            index2 = ipIndex2 + 5
            ip = arpReturn[ipIndex2: ipIndex2 + 13]
            ip = ip.strip()
            testValidity = re.match('192\.168\.87\.\d{1,2}', ip) #regex for accepted IPs
            testInterface = True
            for y in interfaceList:
                if ip == y:
                    testInterface = False
            
            if testValidity is not None and testInterface:
                ipMACList[x][0] = ip
                ipMACList[x][1] = arpReturn[ipIndex2 + 13 + 9:ipIndex2 + 13 + 9 + 17]
                x += 1
                
        except ValueError:
            done2 = True
            
        if done and done2:
            break
    
    x = 0
    while x < len(ipMACList):
        if ipMACList[x][0] == 'None':
            del ipMACList[x]
        x += 1
    
    x = 0
    while x < len(ipMACList):
        ipMACList[x][1] = ipMACList[x][1].replace('-',':')
        x += 1
        
    return ipMACList
'''
while True:
    ipMACList = getPanelList()
    print(ipMACList)
'''
