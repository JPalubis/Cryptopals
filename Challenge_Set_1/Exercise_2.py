from time import time

"""
a = bytes.fromhex("1c0111001f010100061a024b53535009181c")
b = bytes.fromhex("686974207468652062756c6c277320657965")

# print(a)
# print(b)

def iter_1(a, b):
    for i in range(min(len(a), len(b))):
        a[i], b[i]

def iter_2(a, b):
    for byte_1, byte_2 in zip(a, b):
        byte_1, byte_2


def XOR_1(a, b):
    result = b''
    for byte_1, byte_2 in zip(a, b):
        result += bytes((byte_1 ^ byte_2,))
    
    return result

def XOR_2(a, b):
    result = []
    for byte_1, byte_2 in zip(a, b):
        result.append(byte_1 ^ byte_2)
    
    return bytes(result)

def XOR_3(a, b):
    return b''.join(bytes((byte_1 ^ byte_2,)) for byte_1, byte_2 in zip(a, b))

def XOR_4(a, b):
    return bytes(byte_1 ^ byte_2 for byte_1, byte_2 in zip(a, b))
"""


# ===============================================================================================


def _bytes_xor(a: bytes, b: bytes, quiet=True, check_lens=False) -> bytes:
    if not quiet:
        print(a, " xor ", b)
    if check_lens and len(a) != len(b):
        raise ValueError("bytestring lengths aren't equal!")
    return bytes(byte_1 ^ byte_2 for byte_1, byte_2 in zip(a, b))

def bytes_xor(*args: bytes, quiet=True, check_lens=False):
    assert len(args) > 0
    result = args[0]
    for arg in args[1:]:
        result = _bytes_xor(result, arg, quiet=quiet, check_lens=check_lens)
    
    return result


if __name__ == "__main__":
    a = bytes.fromhex("1c0111001f010100061a024b53535009181c")
    b = bytes.fromhex("686974207468652062756c6c277320657965")
    result = bytes_xor(a, b, quiet=False)
    
    print(f"{result = }")
    print(f"{result.hex()}")

    if result == bytes.fromhex("746865206b696420646f6e277420706c6179"):
        print("It worked!")
    else:
        exit("XOR didn't work (this shouldn't happen!)")
