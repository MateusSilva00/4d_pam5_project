from typing import List, Tuple

from src.logger import logger

_BIT2LEVEL = {
    "00": -2,
    "10": -1,
    "01": 1,
    "11": 2,
}


def enconde_4d_pam5(bin_str: str) -> List[Tuple[int, int, int, int]]:
    padding = (8 - len(bin_str) % 8) % 8
    logger.debug(f"Padding needed: {padding} bits")
    bin_str_padded = bin_str + "0" * padding
    logger.debug(f"Padded binary string: {bin_str_padded}")

    symbols = []

    for i in range(0, len(bin_str_padded), 8):
        block = bin_str_padded[i:i + 8]
        logger.debug(f"Processing block: {block}")
        levels = []

        for j in range(0, 8, 2):
            pair = block[j:j + 2]
            logger.debug(f"Bit pair: {pair} - Level: {_BIT2LEVEL[pair]}")
            levels.append(_BIT2LEVEL[pair])
        symbols.append(tuple(levels))
    
    return symbols

if __name__ == "__main__":
    sample_bin = "1100101010110010"
    encoded_symbols = enconde_4d_pam5(sample_bin)
    print(f"Original binary: {sample_bin}")
    print(f"Encoded symbols: {encoded_symbols}")