from os.path import commonprefix

from Exercise_12 import ECBOracleType, main, make_oracle, find_block_size_and_postfix_length, AES

def find_prefix_length(oracle: ECBOracleType, block_size: int) -> int:
    # ct_1 can be optimized, since we add no more then 16 null bytes
    # ct_1 = oracle(b'\x00')
    ct_1 = oracle(bytes(16)) # all-null ciphertext
    ct_2 = oracle(b'\x01')
    eq_blocks = len(commonprefix((ct_1, ct_2))) // block_size
    index = block_size * (eq_blocks + 1)
    for i in range(1, 17):
        ct_3 = oracle(bytes(i) + b'\x01')
        if ct_1[:index] == ct_3[:index]:
            return index - i
    raise Exception("Oh no!")

def wrap_oracle(oracle: ECBOracleType, prefix_len: int, block_size: int) -> ECBOracleType:
    pad_len = block_size - (prefix_len % block_size)
    cutoff_ind = prefix_len + pad_len

    def wrapped_oracle(message: bytes) -> bytes:
        return oracle(bytes(pad_len) + message)[cutoff_ind:]
    
    return wrapped_oracle

if __name__ == "__main__":
    oracle = make_oracle()

    # Step 1: determine sizes of unknown data fields
    block_size, affix_len = find_block_size_and_postfix_length(oracle)
    print(f"{block_size = }")
    print(f"{affix_len = }")
    assert block_size == AES.block_size

    prefix_len = find_prefix_length(oracle, block_size)
    postfix_len = affix_len - prefix_len

    # Step 2: wrap the oracle
    oracle = wrap_oracle(oracle, prefix_len, block_size)
    
    # Same as Exercise_12.py
    pt = main(oracle, postfix_len)
    print("Done!")
    print("Contents of 'unkown-string':\n")
    print(pt.decode("ascii"))
