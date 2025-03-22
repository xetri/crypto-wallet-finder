from ecdsa import SigningKey, SECP256k1
import hashlib
import base58
import requests
from threading import Thread
import os

MAX_THREADS = os.cpu_count() or 1

# Solana RPC endpoint
RPC_ENDPOINT = "https://api.mainnet-beta.solana.com"

def gensolkey():
    # generate a random private key
    private_key = SigningKey.generate(curve=SECP256k1).to_string()

    # convert the private key to a base58-encoded solana private key
    solana_private_key = base58.b58encode(private_key).decode("utf-8")

    # derive the public key from the private key
    vk = SigningKey.from_string(private_key, curve=SECP256k1).get_verifying_key()
    public_key = b"\x04" + vk.to_string()

    # hash the public key using keccak-256 (solana's hash function)
    public_key_hash = hashlib.sha3_256(public_key).digest()

    # extract the solana address from the hashed public key
    solana_address = base58.b58encode(public_key_hash[:32]).decode("utf-8")

    return solana_private_key, solana_address

def check_balance(pubkey):
    """Checks the balance of a Solana address using the Solana RPC API."""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBalance",
        "params": [pubkey]
    }
    response = requests.post(RPC_ENDPOINT, json=payload)
    if response.status_code == 200:
        result = response.json()
        if 'result' in result: return result['result']['value']
    else: print("Error[]")
    return 0

def main():
    while 1:
        key, addr = gensolkey()

        print(key, addr)

        balance = check_balance(addr)
        if balance > 0:
            print("FOUND Solana:")
            f = open("founds.txt", "a+")
            f.write(addr + " || " +  key + "\n")
            f.close()


print("Searching SOL:>")
for _ in range(MAX_THREADS):
    Thread(target=main).start()
