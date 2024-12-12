#!/usr/bin/env python3
# apt-get install python3-psutil

import argparse
import re

import psutil


def convert_bytes(bytes):
    """Converts bytes to human-readable format (GiB or TiB)."""
    if bytes >= 2**40:
        return f"{bytes / 2**40:7.2f} TiB"
    else:
        return f"{bytes / 2**30:7.2f} GiB"


def format_packets(packets):
    """Formats packets with scientific notation or integer."""
    if packets >= 1000000:
        return f"{packets:8.2e} packets"
    else:
        return f"{packets:8d} packets"


def get_net_stats(pattern):
    net_io_counters = psutil.net_io_counters(pernic=True)

    filtered_interfaces = [
        interface for interface in net_io_counters if pattern.search(interface)
    ]
    max_interface_len = max(len(interface) for interface in filtered_interfaces)

    for interface, stats in net_io_counters.items():
        if pattern.search(interface):
            print(
                f"{interface:{max_interface_len}} : RX {convert_bytes(stats.bytes_recv)}, {format_packets(stats.packets_recv)}, TX {convert_bytes(stats.bytes_sent)}, {format_packets(stats.packets_sent)}"
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Display network interface statistics."
    )
    parser.add_argument(
        "-p", "--pattern", default=".*", help="Filter interfaces by regex pattern"
    )
    args = parser.parse_args()

    pattern = re.compile(args.pattern)
    get_net_stats(pattern)
