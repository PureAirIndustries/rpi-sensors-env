""" This is a semaphore implementation for running the following processes
    from the alphasense scs_


    To run

"""
import os
import threading
import time
import json
from publisher import GenerateAWSClientConnection

mutex = threading.Lock() # vs threading.Semaphore()
aws_connection = GenerateAWSClientConnection(
    "rpi-sensors-env/SCS/aws/certs/root-CA.crt",
    "rpi-sensors-env/SCS/aws/certs/PAI_sensing_station.private.key",
    "rpi-sensors-env/SCS/aws/certs/PAI_sensing_station.cert.pem"
)

gases_sampler_cli = os.system("/gases_sampler -i 10 ")
particulates_sampler_cli = os.system("/gases_sampler -i 10")

def sample_gas():
    while True:
        mutex.acquire()
        os.system("/gases_sampler -i 10")
        aws_connection.publish('gas up', '')
        mutex.release()
        time.sleep(0.5)

def sample_particulates():
    while True:
        mutex.acquire()
        particulates_sampler_cli
        aws_connection.publish('particulates up', '')
        mutex.release()
        time.sleep(0.5)


t1 = threading.Thread(target=sample_gas).start()
t2 = threading.Thread(target=sample_particulates).start()
