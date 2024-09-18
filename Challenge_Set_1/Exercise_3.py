"""from collections import Counter
from string import ascii_lowercase, ascii_uppercase, ascii_letters

with open("frankenstein.txt", encoding="utf-8") as f:
    book = f.read()

print(len(book))

def get_frequencies(text, letters):
    counts = Counter()
    for letter in letters:
        counts[letter] += text.count(letter)
    total = sum(counts.values())

    return {letter: counts[letter] / total for letter in letters}

# print(get_frequencies(book, ascii_lowercase))
# print(get_frequencies(book, ascii_uppercase))
print(get_frequencies(book, ascii_letters)) """


# ==============================================================================================


from dataclasses import dataclass, astuple
from typing import Optional
from Exercise_2 import bytes_xor
from pprint import pprint

lower_frequencies = {'a': 0.07567688804030273, 
               'b': 0.013704538657955878, 
               'c': 0.026054726139265256, 
               'd': 0.048092406431874124, 
               'e': 0.1316251063927676, 
               'f': 0.024461710105587633, 
               'g': 0.01661740010581767, 
               'h': 0.05591371259000253, 
               'i': 0.06151514802972096, 
               'j': 0.0012393319684387294, 
               'k': 0.004971705274780888, 
               'l': 0.036205171263601024, 
               'm': 0.029436290860573717, 
               'n': 0.06964125508959997, 
               'o': 0.07211991902647742, 
               'p': 0.017117733661521473, 
               'q': 0.0009287801062777484, 
               'r': 0.05969784454003819, 
               's': 0.059873248832555036, 
               't': 0.08546789813898921, 
               'u': 0.029738216282119114, 
               'v': 0.010883692576660301, 
               'w': 0.021180787191460975, 
               'x': 0.0019409491385061306, 
               'y': 0.02231660187251271, 
               'z': 0.000612477283706379}
"""upper_frequencies = { 
               'A': 0.0012220790872075637, 
               'B': 0.0007332474523245382, 
               'C': 0.0006153527639115732, 
               'D': 0.0003824388672908376, 
               'E': 0.0009172781854569713, 
               'F': 0.0006182282441167675, 
               'G': 0.0005779715212440477, 
               'H': 0.000914402705251777, 
               'I': 0.009155528973338548, 
               'J': 0.000204159094568793, 
               'K': 8.913988636102229e-05, 
               'L': 0.00037668790688044905, 
               'M': 0.0008856479031998344, 
               'N': 0.00040256722872719744, 
               'O': 0.0004974580754986082, 
               'P': 0.0005204619171401624, 
               'Q': 2.8754802051942673e-06, 
               'R': 0.00033068022359734076, 
               'S': 0.0010092935520231879, 
               'T': 0.0018863150146074393, 
               'U': 0.00020128361436359872, 
               'V': 0.00012652112902854776, 
               'W': 0.0008252628188907548, 
               'X': 5.750960410388535e-06, 
               'Y': 0.0004658277932414713, 
               'Z': 0.0} """

@dataclass(order=True)
class ScoredGuess:
    score: float = float("inf")
    key: Optional[int] = None
    ciphertext: Optional[bytes] = None
    plaintext: Optional[bytes] = None

    @classmethod
    def from_key(cls, ct, key_value):
        full_key = bytes([key_value]) * len(ct)
        pt = bytes_xor(ct, full_key)
        score = score_text(pt)

        return cls(score, key_value, ct, pt)

def score_text(text: bytes) -> float:
    score = 0.0
    l = len(text)

    for letter, frequency_expected in lower_frequencies.items():
        frequency_actual = text.count(ord(letter)) / l
        err = abs(frequency_expected - frequency_actual)
        score += err
    """for letter, frequency_expected in upper_frequencies.items():
        frequency_actual = text.count(ord(letter)) / l
        err = abs(frequency_expected - frequency_actual)
        score += err"""
    
    return score

def crack_xor_cypher_simple(ciphertext: bytes) -> ScoredGuess:
    best_guess = ScoredGuess()

    for candidate_key in range(256):
        guess = ScoredGuess.from_key(ciphertext, candidate_key)
        best_guess = min(best_guess, guess)

    if best_guess.key is None or best_guess.plaintext is None:
        exit("no key found (this should never happen)")
    return best_guess

def crack_xor_cypher(ct: bytes) -> ScoredGuess:
    best_guess = ScoredGuess()

    ct_len = len(ct)
    ct_freqs = {b: ct.count(b) / ct_len for b in range(256)}

    for candidate_key in range(256):
        score = 0
        for letter, frequence_expected in lower_frequencies.items():
            score += abs(frequence_expected - ct_freqs[ord(letter) ^ candidate_key])
        guess = ScoredGuess(score, candidate_key)
        best_guess = min(best_guess, guess)

    if best_guess.key is None:
        exit("no key found (this should never happen!)")
    best_guess.ciphertext = ct
    best_guess.plaintext = bytes_xor(ct, bytes([best_guess.key]) * len(ct))

    return best_guess


if __name__ == "__main__":
    ciphertext = bytes.fromhex("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")
    best_guess = crack_xor_cypher(ciphertext)
    score, key, ciphertext, plaintext = astuple(best_guess)
    
    print(f"{key = }")
    print(f"{plaintext = }")
