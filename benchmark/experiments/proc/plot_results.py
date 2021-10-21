import sys
from collections import defaultdict
import matplotlib.pyplot as plt

FIELDS = [
    "Loss",
    "Consensus TPS",
    "Consensus BPS",
    "Consensus latency",
    "End-to-end TPS",
    "End-to-end BPS",
    "End-to-end latency",
]

UNITS = [
    "Throughput (tx/s)",
    "Throughput (B/s)",
    "Latency (ms)",
    "Throughput (tx/s)",
    "Throughput (B/s)",
    "Latency (ms)",
]

results_file = sys.argv[1]
figure_out = sys.argv[2]
figure_title = sys.argv[3]


def load_results(filename):
    with open(filename, "r") as infile:
        lines = infile.readlines()

    lines = [[float(x) for x in line.strip().split(" ")] for line in lines]
    columns = list(zip(*lines))
    assert len(FIELDS) == len(columns)
    return columns


def _plot_single(ax, x, y, label, ylabel):
    ax.grid(True, axis="both", linestyle=":")
    ax.scatter(x, y, label=label)
    ax.legend()
    ax.set_ylabel(ylabel)
    ax.tick_params(axis="y", direction="in")
    ax.tick_params(axis="x", direction="in")


def plot_all(results, outfile, title):
    loss = results[0]
    fig, ax = plt.subplots(len(FIELDS) - 1, figsize=(6, 13))
    for col_name, col_data, cur_ax, cur_unit in zip(FIELDS[1:], results[1:], ax, UNITS):
        _plot_single(cur_ax, loss, col_data, col_name, cur_unit)
    plt.xlabel("Loss rate")
    ax[0].set_title(title)
    plt.tight_layout()
    plt.savefig(outfile)


def main():
    results = load_results(results_file)
    plot_all(results, figure_out, figure_title)


if __name__ == "__main__":
    main()
