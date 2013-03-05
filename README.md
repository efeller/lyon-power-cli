==========================
Lyon Power Measurement CLI
==========================

### About
This is a command line interface (CLI) to the power measurements website in Lyon. It allows to obtain instant power values per server or group of servers.

### Requirements 

Make sure you have Python with the argparse module installed.

### Usage

From home: 

```$ ./power.py auth --username G5K\_USERNAME --password G5K\_PASSWORD --cluster CLUSTER (e.g. hercule) --hosts HOSTS (e.g. 12 34) --granularity GRANULARITY (e.g. 1 for 1 measure/1 second)```

From the G5K frontend: 

```./power noauth --cluster CLUSTER (e.g. hercule) --hosts HOSTS (e.g. 12 34) --granularity GRANULARITY (e.g. 1 for 1 measure/1 second)```
