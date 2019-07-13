#!/usr/bin/env python
import json
from requests import ConnectionError
import requests
import time
import os

connection_timeout = 5

def main():
    x=0
    second = 60
    filename = 'Hello.txt'
    while (x<4):
        response = pinger(filename)
        if (response == False):
            if (x==2):
                msgslack('1','Failed to ping sent to slack')
                x = 0
                time.sleep(second)
            x = x+1
            print ('Failed to ping, waiting for '+str(second)+' seconds before retry')
            time.sleep(second)
        else:
            print ('Status OK recyle check in '+str(second)+' seconds')
            time.sleep(second)

def pinger(filename):
    start_time = time.time()
    while True:
        try:
            headers = {'Content-Type':'application/json','Postmand-Token':'asdasdasd-asdasdasd','cache-control':'no-cache',}
            data = {'FileName': filename,'TransferType':"CDR"}
            data_json = json.dumps(data)
            pinger = {'json_payload': data_json}
            MNOMW = 'http://127.0.0.1:8888/asdasd/asdasd'
            with requests.Session() as session:
                send = requests.post(MNOMW, data=pinger, headers=headers)
                if (send):
                    json_data = send.json() if send and send.status_code == 200 else None
                    if json_data and 'status' in json_data:
                        if 'status' in json_data['status'] == 'OK':
                            return True
                    else:
                        return False
                else:
                    return False
            break
        except ConnectionError:
            if time.time() > start_time + connection_timeout:
                msgslack('2','connection error')
                main()
                return False
            else:
                time.sleep(1)


def msgslack(function,messagecode):
    if (function == '1'):
        print (messagecode)
        return 0
    elif (function == '2'):
        print ('Connection Error')
    else:
        print ('no message')

if __name__ == "__main__":
    main()