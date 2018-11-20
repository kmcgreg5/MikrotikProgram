import paramiko
from ftplib import FTP

def connectSSH(hostname, password, port = '22', username = 'admin'): #create ssh connection with desired host
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, port, username, password)
    return ssh

def ftpSendFile(hostname, password, fileName, username = 'admin', path = '/'): #send file to desired host and path
    fileTransfer = FTP(hostname, username, password)
    fileTransfer.cwd(path)
    file = open(fileName, 'rb')
    fileTransfer.storbinary('STOR ' + fileName, file)
    file.close()
    fileTransfer.quit()

def ftpDeleteFile(hostname, password, fileName, username = 'admin', path = '/'): #delete file from desired host and path
    fileTransfer = FTP(hostname, username, password)
    fileTransfer.cwd(path)
    fileTransfer.delete(fileName)
