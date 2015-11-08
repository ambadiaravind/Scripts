#!/usr/bin/python

import sys
import time
import graphitesend

from docker import Client
cli = Client(base_url='unix://var/run/docker.sock')

for con in cli.containers():
    contName = con['Names'][0].lstrip('/')
    stats_obj = cli.stats(contName,'true')
    count=1

    for stat in stats_obj:
        if count == 1:
            sysUsg_prev = stat['cpu_stats']['system_cpu_usage']
            totUsg_prev = stat['cpu_stats']['cpu_usage']['total_usage']
        if count == 2:
            sysUsg_cur = stat['cpu_stats']['system_cpu_usage']
            totUsg_cur = stat['cpu_stats']['cpu_usage']['total_usage']
            percpuUsg = stat['cpu_stats']['cpu_usage']['percpu_usage'][0]
            memUsage = stat['memory_stats']['usage']
            memLimit = stat['memory_stats']['limit']

 	    cpuDelta = totUsg_cur - totUsg_prev
 	    systemDelta = sysUsg_cur - sysUsg_prev

            memPercent = float(memUsage) / float(memLimit) * 100.0
            cpuPercent = ( float(cpuDelta) / float(systemDelta) ) * len(str(percpuUsg)) * 100.0

            cpuPercent = float(cpuPercent)
            g = graphitesend.init(graphite_port=32774,system_name=contName)
            g.send_list([('cpuUsage', cpuPercent), ('memUsage', memPercent)])
            break 
        count += 1
        time.sleep(5)   
