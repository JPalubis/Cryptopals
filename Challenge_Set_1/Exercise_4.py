from Exercise_3 import crack_xor_cypher, ScoredGuess

if __name__ == "__main__":
    with open("data/4.txt") as f:
        lines = [bytes.fromhex(line.strip()) for line in f]
    
    overall_best = ScoredGuess()

    for line in lines:
        print(end=".", flush=True)
        candidate = crack_xor_cypher(line)
        overall_best = min(overall_best, candidate)
    
    if overall_best.ciphertext is None:
        exit("No ciphertext found (thi sshould never happen!)")
    
    print()
    print(f"{lines.index(overall_best.ciphertext)=}")
    print(f"{overall_best.key = }")
    print(f"{overall_best.plaintext = }")
