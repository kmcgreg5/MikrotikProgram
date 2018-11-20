#Kai McGregor
import sshftpconnection
import panelquery
import time
import sys
import os

def disablePrint(): #disables print function
    sys.stdout = open(os.devnull, 'w')
    
def enablePrint(): #enables print function
    sys.stdout = sys.__stdout__
    
while(True):
    time.sleep(5)
    ipMACList = panelquery.getPanelList() #gets arp table
    panelFound = False
    for x in ipMACList: #searches for panel ip
        if x[0] == "192.168.88.1":
            panelFound = True
            
    if panelFound: #programs panel
        print('Panel Found')
        exceptionVar = True
        while exceptionVar: #uploads required files
            try:
                sshftpconnection.ftpSendFile('192.168.88.1', '', 'routeros-mmips-6.40.9.npk') #downgrade package
                sshftpconnection.ftpSendFile('192.168.88.1', '', 'MTAutoscript.rsc', path = '/flash/') #MTAutoscript file
                sshftpconnection.ftpSendFile('192.168.88.1', '', 'AddTrustExternalCARoot.crt', path = '/flash/') #certificate file
                sshftpconnection.ftpSendFile('192.168.88.1', '', 'certificate-request_key.pem', path = '/flash/') #certificate file
                sshftpconnection.ftpSendFile('192.168.88.1', '', 'COMODORSAAddTrustCA.crt', path = '/flash/') #certificate file
                sshftpconnection.ftpSendFile('192.168.88.1', '', 'COMODORSADomainValidationSecureServerCA.crt', path = '/flash/') #certificate file
                sshftpconnection.ftpSendFile('192.168.88.1', '', 'hotspot_addmydevice_com.crt', path = '/flash/') #certificate file
                exceptionVar = False
                print('Files Uploaded')
            except (OSError, ConnectionResetError):
                print('FTP Failed, Retrying...')
                time.sleep(2)
        
        exceptionVar = True
        print('Panel Resetting...')
        while exceptionVar: #connects to ssh
            try:
                disablePrint()
                ssh = sshftpconnection.connectSSH('192.168.88.1', '')
                enablePrint()
                print('SSH Connected')
                exceptionVar = False
            except paramiko.SSHException:
                enablePrint()
                print('SSH Failed, Retrying...')
                time.sleep(2)
                
        #executes reset commands
        (stdin, stdout, stderr) = ssh.exec_command(':system package downgrade')
        (stdin, stdout, stderr) = ssh.exec_command(':system reset-configuration keep-users=no no-defaults=yes skip-backup=no run-after-reset=flash/MTAutoscript.rsc')
        time.sleep(1)
        ssh.close()

        exceptionVar = True
        while exceptionVar: #Waits until ip is out of the arp table
            time.sleep(2)
            ipMACList = panelquery.getPanelList()
            exceptionVar = False
            for x in ipMACList:
                if x[0] == '192.168.88.1':
                    exceptionVar = True
                    
        print('Panel Done \n \n')
                
