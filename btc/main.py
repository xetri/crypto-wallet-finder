from helper import pvkhex_to_address_compressed, getHexes
from threading import Thread
import apis

def saveAddr(addr, pvhex, balance):
    with open("./found.txt", "a+") as f:
        f.write(f"[{balance}]: {addr} || {pvhex}\n")

def find(pvkhex):
    addr = pvkhex_to_address_compressed(pvkhex)
    balance = apis.getBalance(addr)

    if balance > 0.0:
        print(f"Found [{balance}]: {addr} || {pvkhex}")
        saveAddr(addr, pvkhex, balance)

    print(pvkhex, addr)

# print("Searching BTC:>")

import helper

print(helper.num_to_hex64(128928282982))

# while True:
#     try:
#         ts : list[Thread] = []
#         for pvkhex in getHexes(): 
#             t = Thread(target=find, args=(pvkhex,))
#             t.start()
#             ts.append(t)
#         for t in ts: t.join()
#     except InterruptedError: exit()
#     except Exception as e:
#         print(e)
