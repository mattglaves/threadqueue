#!/usr/bin/python3

import threading
import os, random
import time
from boxsdk import JWTAuth
from boxsdk import Client
from queue import Queue
from itertools import cycle

sdk = JWTAuth.from_settings_file('./38487735_v17qtrdu_config.json')

Box = Client(sdk)
API_users = cycle((
    Box.user(user_id='6713645944'),
    Box.user(user_id='6713647144'),
    Box.user(user_id='6713648344'),
    Box.user(user_id='6713649544'),
    Box.user(user_id='6713650744'),
    Box.user(user_id='6713651944'),
    Box.user(user_id='6713653144'),
    Box.user(user_id='6713654344'),
    Box.user(user_id='6713655544'),
    Box.user(user_id='6713656744'),
    Box.user(user_id='6713657944'),
    Box.user(user_id='6713659144'),
    Box.user(user_id='6713660344'),
    Box.user(user_id='6713661544'),
    Box.user(user_id='6713662744')))

total_files = 10000
max_threads = 60
target_folder = 61251909299

def upload_file(filename):
    Box.as_user(next(API_users)).folder(folder_id=target_folder).upload("/tmp/files/"+filename, file_name=filename)
    with lock:
        print(threading.current_thread().name,item)

def worker():
    while True:
        upload_file(q.get())
        q.task_done()

def genfiles(count):
    print ("Generating Files",end='',flush=True)
    for genfiles in range(count):
        if not os.path.isfile("/tmp/files/"+str(genfiles)+".bin"):
            os.system("dd if=/dev/zero of=/tmp/files/"+str(genfiles)+".bin bs=1 count="+str(random.randint(200000,400000))+ " status=none")
            print (".",end='',flush=True)
        else:
            print("o",end='',flush=True)
    print (" - done")


genfiles(total_files)

lock = threading.Lock()

print ("Starting Upload")
q = Queue()
for i in range(max_threads):
    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()

start = time.perf_counter()
for item in range(total_files):
    q.put(str(item)+".bin")

q.join()

print('Run Time:',time.perf_counter() - start)
