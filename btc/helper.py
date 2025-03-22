import ecdsa
import codecs, hashlib, binascii, base58
import os, random

from ecdsa.eddsa import bytes_to_int, int_to_bytes

DIFF = 1

def getHexes():
    bases = []

    pk = bytes_to_int(os.urandom(32))
    i = pk - DIFF
    while i <= pk + DIFF:
        hex_string = binascii.hexlify(int_to_bytes(i)).decode()
        bases.append(hex_string)
        i += 1

    pk = int(getRandomHex(), 16) 
    i = pk - DIFF
    while i <= pk + DIFF:
        hex_string = binascii.hexlify(int_to_bytes(i)).decode()
        bases.append(hex_string)
        i += 1

    return bases


def getRandomHex(): return ''.join(random.choice('0123456789abcdef') for _ in range(64))

def num_to_hex64(numkey):
    key = hex(numkey)[2:]
    prefix = "0" * (64 - len(key))
    return prefix + key

def pvkhex_to_address_uncompressed(z):
    zk = ecdsa.SigningKey.from_string(codecs.decode(z, 'hex'), curve=ecdsa.SECP256k1)

    z_public_key = b'\x04' + zk.verifying_key.to_string()

    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(hashlib.sha256(z_public_key).digest())
    ripemd160_result = ripemd160.hexdigest()
    step3 = '00' + ripemd160_result

    second_sha256 = hashlib.sha256(binascii.unhexlify(step3)).hexdigest()

    third_sha256 = hashlib.sha256(binascii.unhexlify(second_sha256)).hexdigest()

    step6 = third_sha256[:8]

    step7 = step3 + step6

    btc_uncompressed_address_std = base58.b58encode(binascii.unhexlify(step7)).decode('utf-8')
    return btc_uncompressed_address_std

def pvkhex_to_address_compressed(z):
    pvk_to_bytes = codecs.decode(z, 'hex')

    key = ecdsa.SigningKey.from_string(pvk_to_bytes, curve=ecdsa.SECP256k1).verifying_key
    key_bytes = key.to_string()
    key_hex = codecs.encode(key_bytes, 'hex').decode('utf-8')

    if ord(bytearray.fromhex(key_hex[-2:])) % 2 == 0: public_key_compressed = '02' + key_hex[0:64]
    else:  public_key_compressed = '03' + key_hex[0:64]

    public_key_in_bytes = codecs.decode(public_key_compressed, 'hex')
    sha256_public_key_compressed = hashlib.sha256(public_key_in_bytes)
    sha256_public_key_compressed_digest = sha256_public_key_compressed.digest()

    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(sha256_public_key_compressed_digest)
    ripemd160_digest = ripemd160.digest()
    ripemd160_hex = codecs.encode(ripemd160_digest, 'hex')

    public_key_compressed_btc_network = b'00' + ripemd160_hex
    public_key_compressed_btc_network_bytes = codecs.decode(public_key_compressed_btc_network, 'hex')

    sha256_one = hashlib.sha256(public_key_compressed_btc_network_bytes)
    sha256_one_digest = sha256_one.digest()
    sha256_two = hashlib.sha256(sha256_one_digest)
    sha256_two_digest = sha256_two.digest()
    sha256_2_hex = codecs.encode(sha256_two_digest, 'hex')
    checksum = sha256_2_hex[:8]
    btc_compressed_address_hex = (public_key_compressed_btc_network + checksum).decode('utf-8')

    btc_compressed_address = base58.b58encode(binascii.unhexlify(btc_compressed_address_hex)).decode(
            'utf-8')
    return btc_compressed_address
