import requests
import base58
import os
from ecdsa import SigningKey, SECP256k1
from Crypto.Hash import keccak
from threading import Thread

MAX_THREADS = os.cpu_count() or 1

# TronGrid API endpoint
TRONGRID_API_ENDPOINT = "https://api.trongrid.io"

def generate_random_tron_address():
    # Generate a valid ECDSA private key using secp256k1
    pk = os.urandom(32)
    sk = SigningKey.from_string(pk, curve=SECP256k1)
    
    # Derive the uncompressed public key (65 bytes, starting with 0x04)
    public_key = sk.get_verifying_key().to_string("uncompressed")
    
    # Keccak-256 hash of the public key
    keccak_hash = keccak.new(digest_bits=256).update(public_key).digest()

    # Take last 20 bytes of the hash as the address
    address_bytes = b'\x41' + keccak_hash[-20:]  # Prepend Tron's 0x41 byte
    
    # Base58Check encode
    tron_address = base58.b58encode_check(address_bytes).decode('utf-8')
    
    return tron_address, pk.hex()

def save(content, filepath): 
    with open(filepath, "a+") as f: f.write(content)

def check_tron_balance(address, pvkey):
    url = f"{TRONGRID_API_ENDPOINT}/v1/accounts/{address}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and len(data['data']) > 0:
            con = f"Active Address: {address} || Key: {pvkey}\n"
            save(con, "active.txt")
            print(con)
            balance = data['data'][0].get('balance', 0)  # Balance in SUN (1 TRX = 1,000,000 SUN)
            return balance
    return 0

def main():
    while 1:
        addr, key = generate_random_tron_address()
        print(addr, key)

        balance = check_tron_balance(addr, key)
        if balance > 0:
            con = f"[{balance}]: {addr} || {key}\n"
            print("FOUND:", con)
            save(con, "founds.txt")


print("Searching TRON:>")
for _ in range(MAX_THREADS):
    Thread(target=main).start()
