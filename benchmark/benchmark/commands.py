from os.path import join

from benchmark.utils import PathMaker


class CommandMaker:
    @staticmethod
    def cleanup():
        return f"rm -r .db-* ; rm .*.json ; mkdir -p {PathMaker.results_path()}"

    @staticmethod
    def clean_logs():
        return f"rm -r {PathMaker.logs_path()} ; mkdir -p {PathMaker.logs_path()}"

    @staticmethod
    def compile():
        return "cargo build --quiet --release --features benchmark"

    @staticmethod
    def generate_key(filename):
        assert isinstance(filename, str)
        return f"./node keys --filename {filename}"

    @staticmethod
    def run_node(keys, committee, store, parameters, debug=False, is_bad=False):
        assert isinstance(keys, str)
        assert isinstance(committee, str)
        assert isinstance(parameters, str)
        assert isinstance(debug, bool)
        v = "-vvv" if debug else "-vv"
        b = "--bad" if is_bad else ""
        return (
            f"./node {v} run --keys {keys} --committee {committee} "
            f"--store {store} --parameters {parameters} {b}"
        )

    @staticmethod
    def run_client(address, size, rate, timeout, nodes=[]):
        assert isinstance(address, str)
        assert isinstance(size, int) and size > 0
        assert isinstance(rate, int) and rate >= 0
        assert isinstance(nodes, list)
        assert all(isinstance(x, str) for x in nodes)
        nodes = f'--nodes {" ".join(nodes)}' if nodes else ""
        return (
            f"./client {address} --size {size} "
            f"--rate {rate} --timeout {timeout} {nodes}"
        )

    @staticmethod
    def kill():
        return "tmux kill-server"

    @staticmethod
    def alias_binaries(origin):
        assert isinstance(origin, str)
        node, client = join(origin, "node"), join(origin, "client")
        return f"rm node ; rm client ; ln -s {node} . ; ln -s {client} ."

    @staticmethod
    def remove_loss():
        remove_loss_cmd = """# iptables
sudo iptables -P INPUT ACCEPT
sudo iptables -P FORWARD ACCEPT
sudo iptables -P OUTPUT ACCEPT
sudo iptables -t nat -F
sudo iptables -t mangle -F
sudo iptables -F
sudo iptables -X
# ip6tables
sudo ip6tables -P INPUT ACCEPT
sudo ip6tables -P FORWARD ACCEPT
sudo ip6tables -P OUTPUT ACCEPT
sudo ip6tables -t nat -F
sudo ip6tables -t mangle -F
sudo ip6tables -F
sudo ip6tables -X
"""
        return remove_loss_cmd

    @staticmethod
    def add_loss(rate, sports=None, dports=None):
        assert sports or dports

        def _create_port_matching_rule(ports, port_type, chain):
            assert port_type in ["sport", "dport"]
            if "," in ports:
                # A set of ports
                port_selection = "--match multiport {negation}--{port_type}s {ports}"
            else:
                # A single port or a port range
                port_selection = "{negation}--{port_type} {ports}"
            if "!" in ports:
                negation = "! "
            else:
                negation = ""
            ports = ports.replace("!", "")
            port_selection = port_selection.format(
                ports=ports, negation=negation, port_type=port_type
            )
            add_loss_cmd = f"sudo iptables -t mangle -A {chain} -p tcp {port_selection} -m statistic --mode random --probability {rate} -j DROP"
            return add_loss_cmd

        add_loss_rule = ""
        if sports:
            sport_rule = _create_port_matching_rule(
                ports=sports, port_type="sport", chain="OUTPUT"
            )
            add_loss_rule += sport_rule + "\n"
        if dports:
            dport_rule = _create_port_matching_rule(
                ports=dports, port_type="dport", chain="PREROUTING"
            )
            add_loss_rule += dport_rule
        return add_loss_rule
