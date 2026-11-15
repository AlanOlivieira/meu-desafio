"""Gera as duas figuras do artigo a partir das medições arquivadas.

Requer Python 3 e Matplotlib. Na raiz do repositório, execute
python3 artigo/gerar_figuras.py
"""

from collections import defaultdict
from csv import DictReader
from decimal import Decimal
from pathlib import Path
from statistics import median
import json
import re

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch, Rectangle


ARTICLE = Path(__file__).resolve().parent
REPO = ARTICLE.parent
OUTPUT = ARTICLE / "img"
VERSIONS = {"original": "306ae69", "otimizada": "5c692fc"}
SERIES = {5: "09", 20: "08", 40: "10"}

ORIGINAL = "#3C5984"
OPTIMIZED = "#087469"
PALETTE = {"original": ORIGINAL, "otimizada": OPTIMIZED}
INK = "#142940"
MUTED = "#516579"
RULE = "#D7E1EC"
CANVAS = "#F8FAFD"
PAPER = "#FFFFFF"
PLOT_GRID = "#DDE6EF"
FEATURED = "#EDF3FA"
PAIR = "#A3B1C0"
MONO = "DejaVu Sans Mono"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "text.color": INK,
    "figure.facecolor": CANVAS,
    "savefig.facecolor": CANVAS,
    "savefig.dpi": 150,
})


def pt(number, places):
    return f"{number:,.{places}f}".translate(str.maketrans(",.", ".,"))


def load_runs():
    grouped = {}
    for load, series in SERIES.items():
        pattern = f"*-{series}-validacao-*-{load}vus"
        folders = sorted((REPO / "resultados").glob(pattern))
        runs = defaultdict(list)
        order = []
        for folder in folders:
            version = folder.name.split("-")[-2]
            context = (folder / "contexto.txt").read_text()
            assert f"commit: {VERSIONS[version]}" in context, folder
            assert f"vus: {load}\n" in context, folder
            assert "duracao: 60s" in context and "semente: 42" in context, folder
            summary = (folder / "resumo.txt").read_text()
            rps = Decimal(re.search(r"^Requisições/s:\s+([\d.]+)", summary, re.M)[1])
            p95 = Decimal(re.search(r"^Tempo de resposta:.*\| p95 ([\d.]+) ms", summary, re.M)[1])
            k6 = json.loads((folder / "resumo-k6.json").read_text())["metrics"]
            assert rps == Decimal(f'{k6["http_reqs"]["values"]["rate"]:.2f}'), folder
            assert p95 == Decimal(f'{k6["http_req_duration"]["values"]["p(95)"]:.1f}'), folder
            runs[version].append({"p95": p95 / 1000, "rps": rps, "folder": folder})
            order.append(version)
        if order != ["original", "otimizada"] * 3:
            raise ValueError(f"Esperadas três duplas alternadas em resultados/ para {load} VUs.")
        grouped[load] = runs
    return grouped


def text(fig, x, y, value, size, *, color=INK, weight="normal", align="left", family=None):
    fig.text(x, y, value, fontsize=size, color=color, fontweight=weight,
             ha=align, va="center", fontfamily=family)


def line(fig, x0, x1, y0, y1, color=RULE, width=1.0, style="-", zorder=2):
    fig.add_artist(Line2D([x0, x1], [y0, y1], transform=fig.transFigure,
                          color=color, linewidth=width, linestyle=style, zorder=zorder))


def box(fig, x, y, w, h, *, fill=PAPER, border=RULE, radius=.012, zorder=0):
    fig.add_artist(FancyBboxPatch(
        (x, y), w, h, boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=fill, edgecolor=border, linewidth=.8, transform=fig.transFigure,
        zorder=zorder,
    ))


def marker(fig, x, y, shape, color, size=7):
    fig.add_artist(Line2D([x], [y], marker=shape, markersize=size,
                          color=color, markeredgecolor=PAPER,
                          markeredgewidth=.7, linestyle="none",
                          transform=fig.transFigure, zorder=4))


def heading(fig, title, subtitle):
    text(fig, .062, .927, title, 30, weight="bold")
    text(fig, .063, .865, subtitle, 13.2, color=MUTED)


def version_legend(fig, y):
    marker(fig, .067, y, "o", ORIGINAL, 8)
    text(fig, .079, y, "Original", 12)
    marker(fig, .181, y, "o", OPTIMIZED, 8)
    text(fig, .193, y, "Otimizada", 12)


def save(fig, name):
    fig.savefig(OUTPUT / name, dpi=150)
    plt.close(fig)


def performance_figure(runs):
    fig = plt.figure(figsize=(16, 9))
    heading(fig, "Latência e vazão da API sob carga",
            "Três pares de rodadas alternadas em cada nível de usuários virtuais")
    version_legend(fig, .787)
    line(fig, .325, .357, .787, .787, color=PAIR, width=1.4)
    marker(fig, .325, .787, "o", ORIGINAL, 6)
    marker(fig, .357, .787, "o", OPTIMIZED, 6)
    text(fig, .37, .787, "Par de rodadas", 12)
    marker(fig, .524, .787, "D", INK, 8)
    text(fig, .536, .787, "Mediana", 12)
    line(fig, .062, .938, .746, .746)
    text(fig, .062, .697, "Carga", 12.4, weight="bold")

    panel_specs = (
        ("p95", "Latência p95 (s)", .160, .352, 64, range(0, 61, 10), 4),
        ("rps", "Vazão (req/s)", .567, .361, 8.2, range(0, 9, 2), 2),
    )
    plot_axes = []
    for metric, title, left, width, xmax, ticks, places in panel_specs:
        text(fig, left, .697, title, 16.4, weight="bold")
        ax = fig.add_axes((left, .177, width, .475))
        plot_axes.append(ax)
        ax.set_xlim(0, xmax)
        ax.set_ylim(-.51, 2.51)
        ax.set_facecolor(PAPER)
        ax.axhspan(.50, 1.50, facecolor=FEATURED, edgecolor="none", zorder=0)
        for x in ticks:
            ax.axvline(x, color=PLOT_GRID, linewidth=.8, zorder=1)
        for y in (.50, 1.50):
            ax.axhline(y, color=RULE, linewidth=.7, zorder=1)
        ax.set_xticks(ticks)
        ax.tick_params(axis="x", colors=MUTED, length=3, pad=7, labelsize=11)
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color(RULE)
            spine.set_linewidth(.75)

        for load, center in zip(SERIES, (2, 1, 0)):
            original = [r[metric] for r in runs[load]["original"]]
            optimized = [r[metric] for r in runs[load]["otimizada"]]
            for offset, before, after in zip((.315, .173, .031), original, optimized):
                y = center + offset
                ax.plot([float(before), float(after)], [y, y],
                        linewidth=1.28, color=PAIR, zorder=2)
                ax.scatter([float(before), float(after)], [y, y], s=50,
                           color=[ORIGINAL, OPTIMIZED], edgecolors=PAPER,
                           linewidths=.65, zorder=3)
            for values, color in ((original, ORIGINAL), (optimized, OPTIMIZED)):
                value = median(values)
                ax.scatter([float(value)], [center - .164], s=102, marker="D",
                           color=color, edgecolors=PAPER, linewidths=.9, zorder=4)
                alignment = "center"
                if metric == "p95" and value < 4:
                    alignment = "left"
                elif metric == "p95" and value > Decimal("59.5"):
                    alignment = "right"
                ax.text(float(value), center - .347, pt(value, places), color=color,
                        fontsize=11.3, fontweight="bold", ha=alignment, va="center", zorder=5)

    for load, center in zip(SERIES, (2, 1, 0)):
        display = plot_axes[0].transData.transform((0, center))
        _, y = fig.transFigure.inverted().transform(display)
        text(fig, .062, y + (.014 if load == 20 else 0), f"{load} VUs", 14.3, weight="bold")
        if load == 20:
            text(fig, .062, y - .025, "Cenário principal", 9.2, color=MUTED)

    line(fig, .062, .938, .091, .091)
    text(fig, .062, .051, "Dados dos 18 resumos em resultados/. p95 convertido de ms para s.",
         10.2, color=MUTED)
    text(fig, .938, .051, "306ae69  /  5c692fc", 9.8, color=MUTED, align="right", family=MONO)
    save(fig, "desempenho-por-carga.png")


def resource_medians(runs):
    results = {}
    for version, records in runs[20].items():
        samples_by_service = defaultdict(list)
        for r in records:
            folder = r["folder"]
            context = (folder / "contexto.txt").read_text()
            limits = dict((name, (cpu, memory)) for name, cpu, memory in re.findall(
                r"^  (banco|api): cpus=(\d+) .*? memoria=(\d+) bytes", context, re.M
            ))
            assert limits == {"banco": ("1000000000", "536870912"),
                              "api": ("500000000", "268435456")}, folder

            samples = defaultdict(list)
            with (folder / "recursos.csv").open(newline="") as source:
                for row in DictReader(source):
                    service = row["container"].split("-")[-2]
                    memory = re.fullmatch(r"([\d.]+)\s*MiB", row["memoria"].split(" / ")[0])
                    samples[service].append((Decimal(row["cpu_percentual"].rstrip("%")), Decimal(memory[1])))

            for row in (folder / "recursos.txt").read_text().splitlines():
                match = re.fullmatch(
                    r"\S+-(api|banco)-1\s+(\d+)\s+([\d.]+)%\s+[\d.]+%\s+([\d.]+) MiB\s+[\d.]+ MiB",
                    row,
                )
                if match:
                    service, count, cpu, memory = match.groups()
                    count = int(count)
                    means = (Decimal(cpu), Decimal(memory))
                    for reported, values in zip(means, zip(*samples[service][:count])):
                        assert len(values) == count
                        assert abs(reported - sum(values) / count) <= Decimal(".05"), folder
                    samples_by_service[service].append((means[0] / 100, means[1]))

        assert samples_by_service.keys() == {"api", "banco"}
        assert all(len(values) == 3 for values in samples_by_service.values())
        results[version] = {service: tuple(median(c) for c in zip(*values))
                            for service, values in samples_by_service.items()}
    return results


def resource_figure(values):
    fig = plt.figure(figsize=(16, 9))
    heading(fig, "CPU e memória com 20 usuários virtuais",
            "As barras mostram a proporção da cota. Os rótulos mostram o uso em CPU ou MiB.")
    version_legend(fig, .787)
    text(fig, .938, .787, "Mediana do uso médio de três rodadas por versão", 11.3,
         color=MUTED, align="right")
    cards = (
        ("banco", "Banco · CPU", 0, Decimal(1), "1 CPU", .062, .463),
        ("banco", "Banco · memória", 1, Decimal(512), "512 MiB", .516, .463),
        ("api", "API · CPU", 0, Decimal(".5"), "0,5 CPU", .062, .157),
        ("api", "API · memória", 1, Decimal(256), "256 MiB", .516, .157),
    )
    for service, title, index, quota, quota_label, left, bottom in cards:
        box(fig, left, bottom, .422, .263, fill=PAPER)
        text(fig, left + .025, bottom + .219, title, 16.7, weight="bold")
        text(fig, left + .397, bottom + .219, f"Cota {quota_label}", 11.7,
             color=MUTED, align="right")
        start = left + .027
        track = .276
        for version, offset in (("original", .146), ("otimizada", .088)):
            value = values[version][service][index]
            ratio = value / quota
            assert 0 <= ratio <= 1
            y = bottom + offset
            for bar_width, fill, z in ((track, FEATURED, 1),
                                       (track * float(ratio), PALETTE[version], 2)):
                fig.add_artist(Rectangle((start, y - .012), bar_width, .024,
                                         facecolor=fill, edgecolor="none",
                                         transform=fig.transFigure, zorder=z))
            displayed = f"{pt(value, 3)} CPU" if index == 0 else f"{pt(value, 1)} MiB"
            text(fig, left + .397, y, displayed, 12.2, weight="bold", color=PALETTE[version], align="right")
        for tick, label in ((0, "0%"), (.5, "50%"), (1, "100%")):
            x = start + tick * track
            text(fig, x, bottom + .034, label, 9.7, color=MUTED, align="center")
        line(fig, start + track, start + track, bottom + .056, bottom + .181,
             color=MUTED, width=1.25, style=(0, (2.2, 1.7)), zorder=3)

    line(fig, .062, .938, .091, .091)
    text(fig, .062, .051, "Médias de recursos.txt conferidas nas amostras de recursos.csv.",
         10.2, color=MUTED)
    save(fig, "recursos-20vus.png")


if __name__ == "__main__":
    runs = load_runs()
    resources = resource_medians(runs)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    performance_figure(runs)
    resource_figure(resources)
    print(f"Figuras gravadas em {OUTPUT}")