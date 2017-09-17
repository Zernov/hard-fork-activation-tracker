#!/usr/bin/env python
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import logging
import csv
import time

#logging.basicConfig()
#logging.getLogger("BitcoinRPC").setLevel(logging.DEBUG)

rpc_user = "bitcoinrpc"
rpc_password = "dfVEkRIkhVNWB1UVhfnrhq2IIcWELXNLcIEHmClN9lwK"
rpc_host = "127.0.0.1:8332"
rpc_connection = AuthServiceProxy("http://%s:%s@%s"%(rpc_user, rpc_password, rpc_host))

i = 273796
n = 300375

while i < n:
    block_hash = rpc_connection.getblockhash(i)
    block_time = rpc_connection.getblock(block_hash)["time"]
    with open('/home/zernov/Documents/blockchain/hard-fork-activation-tracker-local/data.csv', 'a') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([i] + [block_time])
    print("[%d] %d/%d" % (100 * i / n, i, n))
    i += 1
    time.sleep(0.1)
