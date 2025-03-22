import requests

# =>
def __apiurl1(addr) : return "https://blockchain.info/q/addressbalance/" + addr
# => ["balance"]
def __apiurl2(addr) : return "https://api.blockcypher.com/v1/btc/main/addrs/" + addr + "/balance"
# => ["unconfirmed_balance"] + ["confirmed_balance"]
def __apiurl3(addr) : return "https://chainflyer.bitflyer.jp/v1/address/" + addr
# => ["chain_stats"]["funded_txo_count"] + ["chain_stats"]["funded_txo_sum"]
def __apiurl4(addr) : return "https://btcscan.org/api/address/" + addr

apis = [ __apiurl1, __apiurl2, __apiurl3, __apiurl4 ]

def getBalance(addr):
    timeout = 0

    while timeout < 5:
        for api in apis:
            try:
                res = requests.get(api(addr))

                if api.__name__ == __apiurl1.__name__:
                    return int(res.json())
                elif api.__name__ == __apiurl2.__name__:
                    return int(res.json()["balance"])
                elif api.__name__ == __apiurl3.__name__:
                    r = res.json()
                    return int(r["unconfirmed_balance"]) + int(r["confirmed_balance"])
                elif api.__name__ == __apiurl4.__name__:
                    r = res.json()["chain_stats"]
                    return int(r["funded_txo_count"]) + int(r["funded_txo_sum"])

            except KeyboardInterrupt: exit()
            except: pass
            
        timeout += 1

    return 0
