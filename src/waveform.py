from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np


def plot_waveform(
    symbols: List[Tuple[int, int, int, int]], title: str = "4D-PAM5 Waveform"
) -> None:
    plt.style.use("seaborn-v0_8-whitegrid")

    y = []
    for symbol in symbols:
        y.extend(symbol)

    # Criar eixo temporal mais realista
    symbol_duration = 1.0  # duração de cada símbolo
    time_per_level = symbol_duration / 4  # tempo para cada nível no símbolo
    x = np.arange(0, len(y) * time_per_level, time_per_level)

    # Criar figura com estilo profissional
    fig, ax = plt.subplots(figsize=(15, 9), dpi=120)

    # Paleta de cores mais suave e profissional
    colors = ["#E74C3C", "#3498DB", "#2ECC71", "#F39C12", "#9B59B6", "#1ABC9C"]

    # Plotar cada símbolo com cor única
    for i, symbol in enumerate(symbols):
        start_time = i * symbol_duration
        symbol_times = np.arange(
            start_time, start_time + symbol_duration, time_per_level
        )
        symbol_levels = list(symbol)

        # Linha principal do símbolo
        ax.step(
            symbol_times,
            symbol_levels,
            where="post",
            color=colors[i % len(colors)],
            linewidth=2.5,
            alpha=0.8,
            label=f"Símbolo {i + 1}",
        )

        # Preenchimento suave abaixo da linha
        ax.fill_between(
            symbol_times,
            symbol_levels,
            alpha=0.15,
            color=colors[i % len(colors)],
            step="post",
        )

    # Pontos de transição mais elegantes
    ax.scatter(
        x, y, c="#34495E", s=40, zorder=5, alpha=0.7, edgecolors="white", linewidth=1
    )

    # Configurar eixos com melhor formatação
    ax.set_ylim(-2.8, 2.8)
    ax.set_xlim(-0.1, len(symbols) * symbol_duration + 0.1)
    ax.set_yticks([-2, -1, 1, 2])
    ax.set_yticklabels(["-2", "-1", "+1", "+2"], fontsize=13, color="#2C3E50")

    # Personalizar grid mais sutil
    ax.grid(True, alpha=0.25, linestyle="-", linewidth=0.5, color="#BDC3C7")
    ax.set_axisbelow(True)

    # Labels e título refinados
    ax.set_xlabel(
        "Tempo (s)", fontsize=15, fontweight="600", color="#2C3E50", labelpad=10
    )
    ax.set_ylabel(
        "Amplitude", fontsize=15, fontweight="600", color="#2C3E50", labelpad=10
    )
    ax.set_title(title, fontsize=18, fontweight="700", color="#2C3E50", pad=25)

    # Linha de referência zero mais elegante
    ax.axhline(y=0, color="#7F8C8D", linewidth=1.2, alpha=0.6, linestyle="--")

    # Legenda aprimorada
    if len(symbols) <= 6:
        legend = ax.legend(
            loc="upper right",
            frameon=True,
            fancybox=True,
            shadow=True,
            fontsize=11,
            ncol=2 if len(symbols) > 3 else 1,
        )
        legend.get_frame().set_facecolor("#FFFFFF")
        legend.get_frame().set_alpha(0.95)
        legend.get_frame().set_edgecolor("#BDC3C7")

    # Estilo visual refinado
    fig.patch.set_facecolor("#FAFAFA")
    ax.set_facecolor("#FFFFFF")

    # Bordas mais elegantes
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Adicionar informações técnicas
    info_text = f"Símbolos: {len(symbols)} | Níveis: 5 | Duração total: {len(symbols)}s"
    ax.text(
        0.02,
        0.98,
        info_text,
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="top",
        bbox=dict(
            boxstyle="round,pad=0.3", facecolor="#ECF0F1", alpha=0.8, edgecolor="none"
        ),
    )

    plt.tight_layout(pad=2.0)
    plt.show()


if __name__ == "__main__":
    from src.ascii_utils import text_to_binary
    from src.encoder import encoder_4d_pam5

    text = "PAM5"
    binary = text_to_binary(text)
    symbols = encoder_4d_pam5(binary)

    plot_waveform(symbols, title="Sinal 4D-PAM5 - Codificação")
