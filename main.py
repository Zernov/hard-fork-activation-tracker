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
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-t', nargs='?', help='process the datetime of the hard fork in the format of the timestamp.')
    group.add_argument('-d', nargs='?', help='process the datetime of the hard fork in the following format (24h): \'dd.mm.yyyy,hh:mm:ss\'')
    args = parser.parse_args()
    if args.t == None:
        return to_timestamp(args.d)
    else:
        return int(args.t)

def connect(rpc_user, rpc_password, rpc_host):
    return AuthServiceProxy('http://%s:%s@%s'%(rpc_user, rpc_password, rpc_host))

def get_block_time(block_height, rpc_connection):
    block_hash = rpc_connection.getblockhash(block_height)
    return rpc_connection.getblock(block_hash)['time']

def to_timestamp(string):
    return int(datetime.strptime(string, '%d.%m.%Y,%H:%M:%S').strftime('%s'))

def from_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%d.%m.%Y,%H:%M:%S')

target_time = get_arguments()

rpc_connection = connect(rpc_user, rpc_password, rpc_host)
