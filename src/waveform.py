from typing import List, Tuple

import matplotlib.pyplot as plt


def plot_waveform(symbols: List[Tuple[int, int, int, int]], title: str = "4D-PAM5 Waveform") -> None:
    """
    Plot the waveform of 4D-PAM5 symbols.
    
    Args:
        symbols (List[Tuple[int, int, int, int]]): List of 4D-PAM5 symbols.
        title (str): Title of the plot.
    """
    y = []
    for symbol in symbols:
        y.extend(symbol)
    
    x = list(range(len(y)))

    plt.figure(figsize=(12, 6))
    plt.step(x, y, where="mid", label="4D-PAM5 Symbols", linewidth=2)
    plt.ylim(-3, 3)
    plt.yticks([-2, -1, 0, 1, 2])
    plt.grid(True)
    plt.xlabel("Time (units)")
    plt.ylabel("Level")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    from src.ascii_utils import text_to_binary
    from src.encoder import encoder_4d_pam5

    text = "PAM5"
    binary = text_to_binary(text)
    symbols = encoder_4d_pam5(binary)

    plot_waveform(symbols, title="Sinal 4D-PAM5 - Codificação")