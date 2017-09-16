#!/usr/bin/env python
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from datetime import datetime
from sys import argv
import argparse
import logging
import csv
import time

#logging.basicConfig()
#logging.getLogger("BitcoinRPC").setLevel(logging.DEBUG)

rpc_user = "bitcoinrpc"
rpc_password = "dfVEkRIkhVNWB1UVhfnrhq2IIcWELXNLcIEHmClN9lwK"
rpc_host = "127.0.0.1:8332"

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

def connect(rpc_user, rpc_password, rpc_host):
    return AuthServiceProxy('http://%s:%s@%s'%(rpc_user, rpc_password, rpc_host))

def get_block_time(block_height, rpc_connection):
    block_hash = rpc_connection.getblockhash(block_height)
    return rpc_connection.getblock(block_hash)['time']

def to_timestamp(string):
    return int(datetime.strptime(string, '%d.%m.%Y,%H:%M:%S').strftime('%s'))

def from_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%d.%m.%Y,%H:%M:%S')

def update(current_time):
    return current_time + 1
    #return int(datetime.now().strftime('%s'))

rpc_connection = connect(rpc_user, rpc_password, rpc_host)

target_time, initial_block = get_arguments()
if initial_block == None:
    initial_block = rpc_connection.getblockcount()
    current_time = int(datetime.now().strftime('%s'))
else:
    initial_block = int(initial_block)
    current_time = get_block_time(initial_block, rpc_connection)

current_block = initial_block
#TODO asdasd
#approx_time =

while current_time < target_time:
    current_time = update(current_time)
