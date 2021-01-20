#!/usr/bin/python3 -u
import os, sys
import pty
import uuid
import requests
from time import sleep
from tempfile import mkstemp
from subprocess import check_output
import socket
import secrets
import hashlib
from random import randint

COLORS = {
    'header': '\033[95m', 
    'blue': '\033[94m', 
    'cyan': '\033[96m', 
    'green': '\033[92m', 
    'warning': '\033[93m', 
    'fail': '\033[91m', 
    'endc': '\033[0m', 
    'bold': '\033[1m', 
    'underline': '\033[4m', 
    'blink': '\033[5m', 
}

class PoW:
    def __init__(self, difficulty, prefix_length):
        self.difficulty = difficulty
        self.prefix_length = prefix_length
    def get_challenge(self):
        return secrets.token_urlsafe(self.prefix_length)[:self.prefix_length].replace('-', 'b').replace('_', 'a')
    def verify_hash(self, prefix, answer):
        h = hashlib.sha256()
        h.update((prefix + answer).encode())
        bits = ''.join(bin(i)[2:].zfill(8) for i in h.digest())
        return bits.startswith('0' * self.difficulty)

def solve_pow():
    powser = PoW(22, 16)
    prefix = powser.get_challenge()
    print("Solve the proof of work to continue the challenge.")
    print(f'''sha256({prefix} + ???) == {'0'*powser.difficulty}({powser.difficulty})...''')
    answer = input("Answer: ")
    if not powser.verify_hash(prefix, answer):
        print("Wrong Answer.")
        exit(-1)
    return prefix

def my_exec(cmds):
    return check_output(cmds)

def _color(s, color=''):
    return s
    code = COLORS.get(color)
    if code:
        return COLORS['bold'] + code + s + COLORS['endc'] + COLORS['endc']
    else:
        return s

if __name__ == '__main__':
    token = solve_pow()

    name = 'token-%s' % token
    cmds = [
        'sudo', 
        'docker', 'ps', '-q', 
        '-f', 'name=%s' % name
    ]
    container_id = my_exec(cmds)
    if container_id:
        print(_color('[*] Connecting to initialized instance...\n', 'bold'))
        cmds = ['sudo', 'docker', 'ps', '-f', 'name=%s' % name, '--format', '"{{.Ports}}"']
        dport = my_exec(cmds)
        port = int(dport.split(b":")[1].split(b"-")[0]) if b":" in dport else 0
        if port == 0:
            print(_color('Couldn\'t find service port.\n', 'warning'))
            exit(-1)
    else:
        print(_color('[*] Initializing instance...\n', 'bold'))

        cmds = [
            'sudo', 
            'docker', 'rm', '-f', name
        ]
        try:
            with open(os.devnull, 'w') as devnull:
                check_output(cmds, stderr=devnull)
        except:
            pass
        
        port = 0
        cmds = ['sudo', 'docker', 'ps', '--format', '"{{.Ports}}"']
        dockerports = my_exec(cmds)
        dockerports = dockerports.split(b'\n')
        #print(dockerports)
        inuseports = [(int(x.split(b":")[1].split(b"-")[0]) if b":" in x else 0) for x in dockerports]
        while port == 0:
            i = randint(20000,29999)
            if i in inuseports:
                continue
            port = i
            break
        #for i in range(20000,30000):
            
        
        if port == 0:
            print(_color('No more resource.\nPlease try again later.\n', 'warning'))
            exit(-1)
        
        cmds = [
            'sudo', 
            'docker', 'run', '-d', '--rm', 
            '-v', '/home/hoc/share:/home/hoc', '-p', '%d:54321' % port,
            '--name', name, 
            'houseofcsy'
        ]
        my_exec(cmds)
        sleep(2)


    print("Your service is running on port %d.\n"%port)
#    cmds = [
#        'nc', '127.0.0.1', str(port)
#    ]

#    pty.spawn(cmds)
    '''
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", port))
    os.dup2(sock.fileno(),0)
    os.dup2(sock.fileno(),1)
    #os.dup2(0,sock.fileno())
    #os.dup2(1,sock.fileno())
    while True:
        continue
    '''
    