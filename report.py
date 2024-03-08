import sys
import json
from texttable import Texttable

def load_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def wrap_text(text_list, width=10):
    return '\n'.join([text_list[i:i+width] for i in range(0, len(text_list), width)])

def generate_report(data, output_file):
    with open(output_file, 'w') as out:

        out.write("Domain Information:\n")
        table = Texttable(max_width=0)
        headers = ["Domain", "Geo Location", "HSTS", "HTTP Server", "Insecure\nHTTP", "IPv4 Addresses", "IPv6 Addresses", "RDNS Names", "Redirect\nto HTTPS", "Root CA", "Scan Time", "TLS Versions"]
        table.set_cols_align(["l"] * len(headers))
        table.set_cols_valign(["m"] * len(headers))
        table.add_row(headers)

        for domain, details in data.items():
            geo_location = '\n'.join(details["geo_locations"])
            hsts = "Yes" if details["hsts"] else "No"
            http_server = wrap_text(str(details.get("http_server", "N/A")), 10)
            insecure_http = "Yes" if details["insecure_http"] else "No"
            ipv4_addresses = wrap_text(', '.join(details["ipv4_addresses"]), 15)
            ipv6_addresses = wrap_text(', '.join(details["ipv6_addresses"]), 27)
            rdns_names = wrap_text(', '.join(details["rdns_names"]), 30)
            redirect_to_https = "Yes" if details["redirect_to_https"] else "No"
            root_ca = wrap_text(str(details.get("root_ca", "N/A")), 12)
            scan_time = details.get("scan_time", "N/A")
            tls_versions = wrap_text(', '.join(details["tls_versions"]), 9)

            table.add_row([domain, geo_location, hsts, http_server, insecure_http, ipv4_addresses, ipv6_addresses, rdns_names, redirect_to_https, root_ca, scan_time, tls_versions])
        out.write(table.draw() + "\n\n")

        # RTT Ranges Section
        out.write("RTT Ranges (Fastest to Slowest):\n")
        rtt_table = Texttable()
        rtt_table.set_cols_align(["l", "l"])
        rtt_table.set_cols_valign(["m", "m"])
        rtt_table.add_row(["Domain", "RTT Range (ms)"])
        rtt_ranges = [(domain, "rtt_range") for domain, details in data.items()]
        rtt_ranges.sort(key=lambda x: x[1][0])
        for domain, rtt_range in rtt_ranges:
            rtt_table.add_row([domain, rtt_range])
        out.write(rtt_table.draw() + "\n\n")

        # Root Certificate Authorities Section
        out.write("Root Certificate Authorities (Most to Least Popular):\n")
        ca_counts = {}
        for details in data.values():
            ca = details.get("root_ca")
            if ca:
                ca_counts[ca] = ca_counts.get(ca, 0) + 1
        ca_table = Texttable()
        ca_table.set_cols_align(["l", "r"])
        ca_table.set_cols_valign(["m", "m"])
        ca_table.add_row(["Root CA", "Occurrences"])
        for ca, count in sorted(ca_counts.items(), key=lambda x: x[1], reverse=True):
            ca_table.add_row([ca, count])
        out.write(ca_table.draw() + "\n\n")

        # Web Servers Section
        out.write("Web Servers (Most to Least Popular):\n")
        server_counts = {}
        for details in data.values():
            server = details.get("http_server")
            if server:
                server_counts[server] = server_counts.get(server, 0) + 1
        server_table = Texttable()
        server_table.set_cols_align(["l", "r"])
        server_table.set_cols_valign(["m", "m"])
        server_table.add_row(["Web Server", "Occurrences"])
        for server, count in sorted(server_counts.items(), key=lambda x: x[1], reverse=True):
            server_table.add_row([server, count])
        out.write(server_table.draw() + "\n\n")

        # TLS Support Section
        out.write("Domain Support Percentages:\n")
        support_types = ["SSLv2", "SSLv3", "TLSv1.0", "TLSv1.1", "TLSv1.2", "TLSv1.3", "plain http", "https redirect", "hsts", "ipv6"]
        tls_counts = dict.fromkeys(support_types, 0)
        total_domains = len(data)
        for details in data.values():
            for support_type in support_types:
                if any(support_type == x for x in ["SSLv2", "SSLv3", "TLSv1.0", "TLSv1.1", "TLSv1.2", "TLSv1.3"]):
                    if support_type in details.get("tls_versions", False):
                        tls_counts[support_type] += 1
                elif support_type == "plain http":
                    if details.get("insecure_http", False):
                        tls_counts[support_type] += 1
                elif support_type == "https redirect":
                    if details.get("redirect_to_https", False):
                        tls_counts[support_type] += 1
                elif support_type == "hsts":
                    if details.get(support_type, False):
                        tls_counts[support_type] += 1
                elif support_type == "ipv6":
                    if len(details.get("ipv6_addresses", False)) > 0:
                        tls_counts[support_type] += 1
                    
        tls_table = Texttable()
        tls_table.set_cols_align(["l", "r"])
        tls_table.set_cols_valign(["m", "m"])
        tls_table.add_row(["TLS Version", "Support Percentage"])
        for version in support_types:
            percentage = (tls_counts[version] / total_domains) * 100
            tls_table.add_row([version, f"{percentage:.2f}%"])
        out.write(tls_table.draw())

def main():
    if len(sys.argv) != 3:
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    data = load_data(input_file)
    generate_report(data, output_file)

if __name__ == "__main__":
    main()