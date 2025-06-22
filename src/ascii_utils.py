def text_to_binary(text: str) -> str:
    binary = []
    for char in text:
        binary.append(format(ord(char), '08b'))
    return ''.join(binary)

def binary_to_text(binary: str) -> str:
    text = []
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        text.append(chr(int(byte, 2)))
    return ''.join(text)


if __name__ == "__main__":
    sample_text = "Hello world!"
    binary = text_to_binary(sample_text)
    reconverted_text = binary_to_text(binary)
    print(f"Original text: {sample_text}")
    print(f"Binary representation: {binary}")
    print(f"Reconverted text: {reconverted_text}")