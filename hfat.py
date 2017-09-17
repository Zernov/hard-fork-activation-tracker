#!/usr/bin/env python
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from sys import argv
import datetime
import argparse
import logging
import csv
import time
import sys

#logging.basicConfig()
#logging.getLogger("BitcoinRPC").setLevel(logging.DEBUG)
#max_height = 300374, max_timestamp = 1399882427, max_datetime = 12.05.2014,12:13:47

def connect(rpc_user, rpc_password, rpc_host):
    return AuthServiceProxy('http://%s:%s@%s'%(rpc_user, rpc_password, rpc_host))

def get_arguments():
    parser = argparse.ArgumentParser(description='hard fork activation tracker')
    hard_fork = parser.add_mutually_exclusive_group(required=True)
    hard_fork.add_argument('-t', nargs='?', help='process the datetime of the hard fork in the format of the timestamp')
    hard_fork.add_argument('-d', nargs='?', help='process the datetime of the hard fork in the following format (24h): \'dd.mm.yyyy,hh:mm:ss\'')
    parser.add_argument('-b', nargs='?', help='number of the initial block')
    args = parser.parse_args()
    if args.t == None:
        args.t = to_timestamp(args.d)
    return int(args.t), args.b

def get_block_time(block_height):
    block_hash = rpc_connection.getblockhash(block_height)
    return rpc_connection.getblock(block_hash)['time']

def get_block_time_mtp(block_height):
    block_hashes = rpc_connection.batch_([ [ 'getblockhash', height ] for height in range(block_height - 11, block_height) ])
    blocks = rpc_connection.batch_([ [ 'getblock', h ] for h in block_hashes ])
    block_times = [ block['time'] for block in blocks ]
    return sorted(block_times)[5]

def update_time(current_time):
    return int(datetime.now().strftime('%s')) if real_time else current_time + 60

def new_block_mined(current_time, current_block):
    return rpc_connection.getblockcount != current_block if real_time else get_block_time(current_block + 1) <= current_time

def get_average_time(current_block):
    return (get_block_time(current_block) - get_block_time_mtp(current_block))

def to_timestamp(string):
    return int(datetime.datetime.strptime(string, '%d.%m.%Y,%H:%M:%S').strftime('%s'))

def to_datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%d.%m.%Y,%H:%M:%S')

def to_time(timestamp):
    return str(datetime.timedelta(seconds=timestamp))

rpc_user = "bitcoinrpc"
rpc_password = "dfVEkRIkhVNWB1UVhfnrhq2IIcWELXNLcIEHmClN9lwK"
rpc_host = "127.0.0.1:8332"
rpc_connection = connect(rpc_user, rpc_password, rpc_host)
real_time = False
target_time, initial_block = get_arguments()

if initial_block == None:
    initial_block = rpc_connection.getblockcount()
    current_time = int(datetime.now().strftime('%s'))
    real_time = True
else:
    initial_block = int(initial_block)
    current_time = get_block_time(initial_block)

current_block = initial_block
current_block_time_mtp = get_block_time_mtp(current_block)
approx = get_average_time(current_block)
border_block_time = target_time
mined_blocks = 0
before_target_time = current_time < target_time

print("\nTarget time: %s" % (to_datetime(target_time)))

while current_block_time_mtp < target_time:
    current_time = update_time(current_time)
    if new_block_mined(current_time, current_block):
        current_block = current_block + 1
        current_block_time_mtp = get_block_time_mtp(current_block)
        if current_time > target_time and before_target_time:
            before_target_time = False
            border_block_time = get_block_time(current_block)
        mined_blocks = mined_blocks + 1
        approx = (approx * mined_blocks + get_average_time(current_block)) / (mined_blocks + 1)
    left = approx + border_block_time - current_time
    sys.stdout.write("\rCurrent time: %s | Time left: %s | Approx: %s      " % (to_datetime(current_time), ("-" if left < 0 else "+") + to_time(abs(left)), approx))
    sys.stdout.flush()

print("\n\n[ Activation time ]")
print(" The block #%s" % (current_block))
print(" Timestamp: %s" % (to_datetime(get_block_time(current_block))))
print("       MTP: %s" % (to_datetime(current_block_time_mtp)))
print("[ Activation time ]\n")
