#!/usr/bin/env python
import logging,sys
import json
import requests
import paramiko

key = paramiko.RSAKey.from_private_key_file('/Users/bagus/.ssh/forge_rsa')

def connect(hostname, i, key):
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh.connect(hostname, username='bagus', pkey=key, timeout=5)
    command = 'ls '+i
    output = ""
    stdin, stdout, stderr = ssh.exec_command(command, timeout=3)
    stdout=stdout.readlines()
    ssh.close()
    for line in stdout:
        output = output+line
    if output != "":
        return True
    else:
        return False

def getfilelist(checklist):
    lineList = [line.rstrip('\n')
        for line in open(checklist)]
    if lineList == []:
        return lineList
    else:
        lineList = list(dict.fromkeys(lineList))
        return lineList

def sendToapi(i):
    print (i+' not found sending request to API')
    #Do something
    #data = {'filename':i}
    #data_json = json.dumps(data)
    #payload = {'json_payload': data_json, 'apikey': '73AS8S766FASD'}
    send = requests.get('https://jsonplaceholder.typicode.com/todos/1')
    resp = send.headers.get('content-type')
    if resp == 'application/json; charset=utf-8':
        return send
    else:
        return False

if __name__ == "__main__":
    fileTocheck = getfilelist(sys.argv[2])
    if fileTocheck:
        for i in fileTocheck:
            check = connect(sys.argv[1], i, key)
            if check != False:
                print 'OK'
            else:
                send = sendToapi(i)
                if send is False:
                    print ('Response from API invalid')
                else:
                    print send
    else:
        print 'No file list to check with'