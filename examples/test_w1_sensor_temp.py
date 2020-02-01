#!/usr/bin/python3
#file: test_owfs.py
#author: Menschel (C) 2020
#purpose: straight foreward show the basic of the linux one-wire subsystem from the file system

import glob
import os
import re

regex = re.compile("t=\d+")


def get_temp_from_w1_sensor_file(fpath):
    """ read the sensor file and return a scaled temperature value """
    with open(fpath) as f:
        lines = f.readlines()
    for line in lines:
        for elem in regex.findall(line):
            t = int(elem[2:])/1000
            return t
    raise ValueError("No pattern found found")

def get_w1_temp_sensor_values():
    """ find the available one-wire sensors and fetch their values """
    sensor_dict = {}
    for dev in glob.glob("/sys/bus/w1/devices/*"):
        fpath = os.path.join(dev,"w1_slave")
        if os.path.exists(fpath):
            devid = os.path.split(dev)[-1]        
            val = get_temp_from_w1_sensor_file(fpath)
            sensor_dict.update({devid:val})
    return sensor_dict

                

if __name__ == "__main__":
    from pprint import pprint as pp
    pp(get_w1_temp_sensor_values())
