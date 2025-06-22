from src.ascii_utils import binary_to_text, text_to_binary
from src.logger import logger


def xor_binary(bin_str: str, key: str) -> str:
    """
    Perform XOR operation on two binary strings of equal length.
    Example:
        >>> xor_binary("1100", "1010")
        '0110'
    """
    logger.debug(f"Performing XOR on: '{bin_str}' with key: {key}")

    # Ensure both strings are of equal length
    key_repetitions = len(bin_str) // len(key) + 1
    expanded_key = (key * key_repetitions)[: len(bin_str)]

    result = []

    for idx, bit in enumerate(bin_str):
        result_bit = str(int(bit) ^ int(expanded_key[idx]))
        result.append(result_bit)

    xor_result = "".join(result)
    logger.info(f"XOR result: {xor_result}")
    return xor_result


def permute_bits(bin_str: str, seed: int) -> str:
    """
    Permute bits of a binary string based on a seed.
    Example:
        >>> permute_bits("1100", 3)
        '0110'
    """
    shift = seed % len(bin_str)
    logger.debug(f"Shifting bits by {shift} positions")
    permuted = bin_str[shift:] + bin_str[:shift]
    logger.info(f"Permuted bits: {permuted}")
    return permuted


def unpermute_bits(bin_str: str, seed: int) -> str:
    """
    Reverse the permutation of bits based on a seed.
    Example:
        >>> unpermute_bits("0011", 3)
        '1001'
    """
    shift = seed % len(bin_str)
    unpermuted = bin_str[-shift:] + bin_str[:-shift]
    logger.info(f"Unpermuted bits: {unpermuted}")
    return unpermuted


def encrypt_data(message_data: str, key: str) -> str:
    """
    Encrypt a binary string using XOR and permutation.
    """
    logger.debug(f"Encrypting data: {message_data} with key: {key}")
    binary_data = text_to_binary(message_data)
    binary_key = text_to_binary(key)

    xor_result = xor_binary(binary_data, binary_key)

    permuted_result = permute_bits(xor_result, len(key))
    return permuted_result


def decrypt_data(encrypted_data: str, key: str) -> str:
    """
    Decrypt a binary string using reverse permutation and XOR.
    """
    binary_key = text_to_binary(key)
    logger.debug(f"Decrypting data: {encrypted_data} with key: {binary_key}")

    unpermuted_result = unpermute_bits(encrypted_data, len(key))

    decrypted_result = xor_binary(unpermuted_result, binary_key)

    text_result = binary_to_text(decrypted_result)

    return text_result


if __name__ == "__main__":
    original_text = "Hello World!"
    key = "chave123"

    encrypted = encrypt_data(original_text, key)
    decrypted = decrypt_data(encrypted, key)

    print(f"Original:     {original_text}")
    print(f"Encrypted:    {encrypted}")
    print(f"Decrypted:    {decrypted}")
