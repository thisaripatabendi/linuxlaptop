#!/usr/bin/env python
"""
/**
* Copyright (c) 2015, WSO2 Inc. (http://www.wso2.org) All Rights Reserved.
*
* WSO2 Inc. licenses this file to you under the Apache License,
* Version 2.0 (the "License"); you may not use this file except
* in compliance with the License.
* You may obtain a copy of the License at
*
* http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing,
* software distributed under the License is distributed on an
* "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
* KIND, either express or implied. See the License for the
* specific language governing permissions and limitations
* under the License.
**/
"""
import subprocess

import multiprocessing


def getBatteryLevel():

    read_battery_level = open('/sys/class/power_supply/BAT0/capacity', 'r')
    battery_level = read_battery_level.read()
    read_battery_level.close()

    if " " in battery_level[:3]:
        battery_level = battery_level[:2]
    else:
        battery_level = battery_level[:3]

    # print "----- BATTERY LEVEL -----"
    # print(battery_level + "%")
    # print

    return int(battery_level)


def getBatteryStatus():

    read_battery_status = open('/sys/class/power_supply/BAT0/status', 'r')
    battery_status = read_battery_status.read()
    read_battery_status.close()
    battery_status = battery_status.split(' ')[0]

    # charging = 1 / discharging = 0 / battery full = -1

    # if battery_status[:8] == "Charging"
    # unknown status assigns when the battery is full and the device is still plugged into charge
    if battery_status[:7] == "Unknown":
        battery_status = 1
    elif battery_status[:11] == "Discharging":
        battery_status = 0
    else:
        battery_status = 1

    # print "----- BATTERY STATUS -----"
    # print("Battery " + str(battery_status))
    # print

    return battery_status

def getCPUUsage():

    speed_list = []

    proc = subprocess.Popen(["cat", "/proc/cpuinfo"], stdout=subprocess.PIPE)
    out, err = proc.communicate()

    cores = multiprocessing.cpu_count()

    total = 0

    count = 1
    for line in out.split("\n"):

        if "cpu MHz" in line:
            speed = float(line.split(":")[1])

            total += speed

            # only is need to get all usages of each core
            # store data into a 2d array - add core number, processor speed and the total speed of a processor
            speed_list.append([count, speed])
            # print "Processor %d : %s MHz" % (count, speed)
            # break
            count += 1

    average = total / cores
    # TODO get the speed of one core in GHz "speedofone"
    speedofone = 2
    percentage = average * 100 / (speedofone * 1000)

    if percentage > 100:
        percentage = 99

    # sizeofone()
    percentage = round(percentage, 2)

    return percentage
