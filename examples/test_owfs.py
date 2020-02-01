#!/usr/bin/python3
#file: test_owfs.py
#author: Menschel (C) 2020
#purpose: straight foreward show the basic usage of one-wire-server
 
import subprocess
import csv

def get_sensor_values(server = "rpi-0w-1.local",
                      port = 4304,
                      sensors = [],
                      ):
    """ call owread as a subprocess and read its output to get the temperature of a specific DS18B20 sensor
        @param server : the name of owserver
        @param port : the port of owserver
        @param sensors : the sensors of owserver to be read
        @return : a dictionary of {DS18B20:values}
    """

    ret = {}
    for sensor in sensors:
        cmd = r"owread -s {0}:{1} {2}/temperature".format(server,port,sensor)
    
        out = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    
        stdout,stderr = out.communicate()
        #print(stdout,stderr)
        temp_c = None
        if len(stderr) == 0:
            try:
                temp_c = float(stdout)
            except:
                pass
        else:
            print(stderr)
    
        ret.update({sensor:temp_c})
    return ret


def get_sensors(server = "rpi-0w-1.local",
                port = 4304,
               ):
    """ call owdir as a subprocess and read its output to get the available DS18B20 sensors on the server,
        this is basically a glob function,
        @param server : the name of owserver
        @param port : the port of owserver
        @return : a list of DS18B20 sensors
    """

    cmd = r"owdir -s {0}:{1} /".format(server,port)
    out = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout,stderr = out.communicate()
    sensors = [x.strip("/") for x in stdout.decode().split("\n") if x.strip("/").startswith("28.")]
    return sensors

if __name__ == "__main__":
    import time
    import statistics
    sensors = get_sensors()
    with open('sensors.csv', 'w', newline='') as csvfile:
        fieldnames = sensors.copy()
        fieldnames.extend(["min","max","mean","stdev"])
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(60):
            sensors_vals = get_sensor_values(sensors=sensors)
            stat_vals = []
            for sensor in sensors_vals:
                val = sensors_vals.get(sensor)
                print(sensor,val)
                if val is not None:
                    stat_vals.append(val)
            if len(stat_vals)>0:
                print("Statistics:\n{0} Sensors\nmin:{1}\nmean: {2}\nmax:{3}\nstdev:{4}".format(len(stat_vals),min(stat_vals),statistics.mean(stat_vals),max(stat_vals),statistics.stdev(stat_vals)))
                sensors_vals.update({"min":min(stat_vals),
                                "max":max(stat_vals),
                                "mean":statistics.mean(stat_vals),
                                "stdev":statistics.stdev(stat_vals),
                               })
            writer.writerow(sensors_vals)
            time.sleep(30)
        
