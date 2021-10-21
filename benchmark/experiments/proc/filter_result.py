import sys
import re
import matplotlib.pyplot as plt

C_TPS = "Consensus TPS: (.*) tx/s"
C_BPS = "Consensus BPS: (.*) B/s"
C_LAT = "Consensus latency: (.*) ms"
EE_TPS = "End-to-end TPS: (.*) tx/s"
EE_BPS = "End-to-end BPS: (.*) B/s"
EE_LAT = "End-to-end latency: (.*) ms"

FIELDS = [C_TPS, C_BPS, C_LAT, EE_TPS, EE_BPS, EE_LAT]

filename = sys.argv[1]
rate = sys.argv[2]


def load_data():
    with open(filename, "r") as infile:
        data = infile.read()
    return data


def get_results(data):
    all_results = []
    for field in FIELDS:
        all_results.append(_extract_field(field, data))
    return all_results


def _extract_field(field, data):
    result = re.findall(field, data)
    result = [int(x.replace(",", "")) for x in result]
    return result


def results_to_string(results):
    s = ""
    for idx in range(len(results[0])):
        s += f"{rate} "
        for field_res in results:
            s += f"{field_res[idx]} "
        s += "\n"
    return s


def main():
    data = load_data()
    results = get_results(data)
    summary = results_to_string(results)
    print(summary, end="")  # The string already includes \n


if __name__ == "__main__":
    main()
