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
    b"MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc="
    b"MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic="
    b"MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw=="
    b"MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg=="
    b"MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl"
    b"MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA=="
    b"MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw=="
    b"MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8="
    b"MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g="
    b"MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"
]

def enc(ind: Optional[int] = None) -> bytes:
    ...

def dec(iv: bytes, ciphertext: bytes) -> bytes:
    ...

def padding_oracle(iv: bytes, ciphertext: bytes) -> bool:
    ...
