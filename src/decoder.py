from typing import List, Tuple

from src.logger import logger

_LEVEL2BIT = {
    -2: "00",
    -1: "10",
    1: "01",
    2: "11",
}


def decoder_4d_pam5(symbols: List[Tuple[int, int, int, int]]) -> str:
    logger.info(f"Decoding symbols: {symbols}")

    bits = []

    for index, symbol in enumerate(symbols):
        logger.debug(f"Processing symbol {index}: {symbol}")
        for level in symbol:
            bit_pair = _LEVEL2BIT.get(level)
            if bit_pair is None:
                logger.error(f"Invalid level {level} in symbol {symbol}")
                raise ValueError(f"Invalid level {level} in symbol {symbol}")
            logger.debug(f"Level {level} corresponds to bit pair {bit_pair}")
            bits.append(bit_pair)

    bin_str = "".join(bits)

    logger.info(f"Decoded binary string: {bin_str}")
    return bin_str


if __name__ == "__main__":
    from src.ascii_utils import binary_to_text, text_to_binary
    from src.encoder import encoder_4d_pam5

    original = "Hello World!"
    bin_data = text_to_binary(original)
    symbols = encoder_4d_pam5(bin_data)
    recovered_bin = decoder_4d_pam5(symbols)
    recovered_text = binary_to_text(recovered_bin[: len(bin_data)])
