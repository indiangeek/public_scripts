#!/usr/bin/python
import os;
import subprocess;
import re;
from datetime import datetime
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

PROMETHEUS_SERVER = "192.168.1.18:9091"
TARGET_URL = "yahoo.com"
PACKET_COUNT = 50
INTERVAL_MS = 100


def main():
    result = pingcheck(TARGET_URL, PACKET_COUNT, INTERVAL_MS);
    logentry_prometheus(result);

def logentry_prometheus(result):

    #print(result);
    registry = CollectorRegistry()
    loss = Gauge('packet_loss', 'Packet loss', registry=registry)
    loss.set(result.get('loss'))
    if ('avg' in result):
        latency_avg = Gauge('latency_avg', 'Average Latency', registry=registry)
        latency_avg.set(result.get('avg'))
    push_to_gateway(PROMETHEUS_SERVER, job='pingcheck', registry=registry)


def logentry_file(str):
    f = open('ping.log', 'a');
    f.write(str+'\n');
    f.close();

def pingcheck(host, count, interval):
    ping_response = subprocess.Popen(["/bin/ping", "-c"+str(count),  "-w"+str(interval), host], stdout=subprocess.PIPE).stdout.read()
    ## First check if ping failed completely.

    try:
        loss = re.search('.*, ([0-9]+)\%.*',ping_response).group(1);
    except AttributeError as err:
        loss = '100'
        print "100% loss -- "


    dt = datetime.now();
    if (loss != '100') :
        stats  = re.search('mdev = (.+?)\/(.+?)\/(.+)\/.*',ping_response)
        min = stats.group(1);
        avg = stats.group(2);
        max = stats.group(3);
        check_result = {
            "date" : dt.strftime("%c"),
            "loss" : loss,
            "min" : min,
            "avg" : avg,
            "max" : max };
    else:
        print "100% loss"
        check_result = {
            "date" : dt.strftime("%c"),
            "loss" : loss,
            "min" : 0,
            "avg" : 0,
            "max" : 0 };


    return (check_result);


if __name__ == '__main__':
        main()

