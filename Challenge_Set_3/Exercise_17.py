import sys
sys.path.insert(0, '/Users/jlpal/Cryptopals/Cryptopals/Challenge_Set_1')
sys.path.insert(0, '/Users/jlpal/Cryptopals/Cryptopals/Challenge_Set_2')

from Crypto.Cipher import AES
from os import urandom
from base64 import b64decode
from random import choice # This is not totally considered "cryptographically secure"
from typing import Optional

from Exercise_2 import bytes_xor
from Exercise_8 import bytes_to_chunks
from Exercise_9 import pkcs7, strip_pkcs7, PaddingError


BLOCK_SIZE = 16

_key = urandom(16)
iv = urandom(BLOCK_SIZE)

strings = [
    b"MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
    b"MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
    b"MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
    b"MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
    b"MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
    b"MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
    b"MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
    b"MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
    b"MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
    b"MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93",
]

def enc(ind: Optional[int] = None) -> bytes:
    s = choice(strings) if ind is None else strings[ind]
    cipher = AES.new(_key, AES.MODE_CBC, iv)
    return cipher.encrypt(pkcs7(s)) # This is our ciphertext

def _dec(iv: bytes, ciphertext: bytes) -> bytes:
    cipher = AES.new(_key, AES.MODE_CBC, iv)
    return cipher.decrypt(ciphertext) # This is out plaintext

def padding_oracle(iv: bytes, ciphertext: bytes) -> bool:
    plaintext = _dec(iv, ciphertext)
    try:
        strip_pkcs7(plaintext)
    except PaddingError:
        return False
    return True

# Types of attacks
def single_block_attack(iv: bytes, block: bytes, oracle) -> bytes:
    plaintext = b''
    isolating_iv = [0] * BLOCK_SIZE # Meant to hold parts of the plaintext until they are needed

    for pad_len in range(1, BLOCK_SIZE + 1):
        padding_iv = [pad_len ^ b for b in isolating_iv]
        for candidate in range(256):
            padding_iv[-pad_len] = candidate
            new_iv = bytes(padding_iv)
            if oracle(new_iv, block):
                if pad_len == 1:
                    padding_iv[-2] ^= 1
                    new_iv = bytes(padding_iv)
                    if not oracle(new_iv, block):
                        continue # Takes us back to the start of the nested 'for' loop
                plaintext = bytes([candidate ^ pad_len]) + plaintext
                break
        else:
            raise Exception(f"No match found for byte {pad_len}") 
            # This won't occur except in the noisy case, which is unlikely to happen anyway
        
        isolating_iv[-pad_len] = candidate ^ pad_len
    
    # debug code
    decrypted_block = bytes_xor(plaintext, iv)
    print(f"Decrypted block: {decrypted_block}")

    return bytes_xor(plaintext, iv)
        

def padding_oracle_attack(ciphertext: bytes, oracle) -> bytes: # This is for multiple blocks
    plaintext = b''
    block_iv = iv
    blocks = bytes_to_chunks(ciphertext, BLOCK_SIZE)

    for i, block in enumerate(blocks):
        plaintext += single_block_attack(block_iv, block, oracle)
        block_iv = block
    return strip_pkcs7(plaintext)
    # Need to consider when this throws an error

if __name__ == "__main__":
    ciphertext = enc()
    print(f"Ciphertext: {ciphertext}") # debug print
    plaintext = padding_oracle_attack(ciphertext, padding_oracle)
    print(f"Plaintext: {plaintext}")
