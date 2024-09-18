"""def hamming_weight_1(byte):
    return bin(byte).count("1")

def hamming_weight_2(byte):
    weight = 0
    while byte != 0:
        weight += byte & 1
        byte >>= 1
    return weight

def hamming_weight_3(byte):
    byte = (byte & 0x55) + ((byte >> 1) & 0x55)
    byte = (byte & 0x33) + ((byte >> 2) & 0x33)
    byte = (byte & 0x0F) + ((byte >> 4) & 0x0F)
    return byte

def hamming_weight_4(byte):
    weight = 0
    while byte > 0:
        byte &= byte - 1
        weight += 1
    return weight

def get_weights():
    weights = {0: 0}
    pow_2 = 1
    for _ in range(8):
        for k, v in weights.copy().items():
            weights[k + pow_2] = v + 1
        pow_2 <<= 1
    return weights

weights = get_weights()

def hamming_weight_5(byte):
    return weights[byte]


a, b = urandom(100), urandom(100)

def hamming_distance(a, b, hw):
    distance = 0
    for byte in bytes_xor(a, b):
        distance += hw(byte)
    return distance

print(timeit(str(hamming_distance(a, b, hamming_weight_1))))
print(timeit(str(hamming_distance(a, b, hamming_weight_2))))
print(timeit(str(hamming_distance(a, b, hamming_weight_3))))
print(timeit(str(hamming_distance(a, b, hamming_weight_4))))
print(timeit(str(hamming_distance(a, b, hamming_weight_5))))"""


# ===============================================================================================


from os import urandom
from itertools import combinations
from base64 import b64decode
from pprint import pprint
from timeit import timeit

from Exercise_2 import bytes_xor
from Exercise_3 import crack_xor_cypher
from Exercise_5 import repeating_key_xor

def hamming_distance(a: bytes, b: bytes) -> int:
    return sum(weights[byte] for byte in bytes_xor(a, b))

def _get_hamming_weights() -> dict[int, int]:
    weights = {0: 0}
    pow_2 = 1
    for _ in range(8):
        for k, v in weights.copy().items():
            weights[k + pow_2] = v + 1
        pow_2 <<= 1
    return weights

weights = _get_hamming_weights()
MAX_KEYSIZE = 40
def guess_keysize(ct: bytes, num_guesses: int = 1) -> list[tuple[float, int]]:
    def get_score(size: int) -> float:
        chunks = (ct[:size], 
                  ct[size : 2 * size], 
                  ct[2 * size : 3 * size], 
                  ct[3 * size : 4 * size])
        avg = sum(hamming_distance(a, b) for a, b in combinations(chunks, 2)) / 6
        return avg / size
    
    scores = [(get_score(size), size) for size in range(2, MAX_KEYSIZE - 1)]
    scores.sort()
    return scores[:num_guesses]

def crack_repeating_key_xor(ciphertext: bytes, keysize: int) -> tuple[float, bytes]:
    chunks = [ciphertext[i::keysize] for i in range(keysize)]
    cracks = [crack_xor_cypher(chunk) for chunk in chunks]

    combined_sum = sum(guess.score for guess in cracks) / keysize
    key = bytes(guess.key for guess in cracks)
    return combined_sum, key

if __name__ == "__main__":
    print(f"{hamming_distance(b'this is a test', b'wokka wokka!!!') = }\n")
    if hamming_distance(b'this is a test', b'wokka wokka!!!') != 37:
        exit("hammign distance function is broken (this should never happen!)")
    
    with open("data/6.txt") as f:
        b64 = f.read()
    ciphertext = b64decode(b64)

    keysizes = guess_keysize(ciphertext, 5)
    print("Best key size guesses: (confidence, size): ")
    pprint(keysizes)

    candidates = [crack_repeating_key_xor(ciphertext, guess) for _, guess in keysizes]
    candidates.sort()
    best_candidate = candidates[0]
    best_key = best_candidate[1]

    print("Best guess: ")
    print(f"{best_key = }")
    print("Plaintext = \n")
    print(repeating_key_xor(best_key, ciphertext).decode("ascii"))
