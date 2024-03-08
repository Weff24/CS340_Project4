import sys
import subprocess
import time
import json

from scanners.ip_scan import get_ip_scan, get_rdns_scan
from scanners.http_scan import HTTPScanner
from scanners.tls_scan import get_tls_scan, get_root_ca
from scanners.rtt_scan import get_rtt_scan
from scanners.geo_scan import get_loc_scan


def main():
    if len(sys.argv) != 3:
        return

    websites = []
    with open(sys.argv[1]) as input_f:
        for line in input_f:
            websites.append(line.split("\n")[0])

    output_json = {}
    for website in websites:
        website_json = {}

        website_json["scan_time"] = time.time()
        website_json["ipv4_addresses"] = get_ip_scan(website, "ipv4")
        website_json["ipv6_addresses"] = get_ip_scan(website, "ipv6")

        http_scanner = HTTPScanner(website)
        website_json["http_server"], website_json["insecure_http"], website_json["redirect_to_https"], website_json["hsts"] = http_scanner.get_http_scan()

        website_json["tls_versions"] = get_tls_scan(website, 2)

        if any("TLS" in version for version in website_json["tls_versions"]):
            website_json["root_ca"] = get_root_ca(website)
        else:
            website_json["root_ca"] = None

        website_json["rdns_names"] = get_rdns_scan(website_json["ipv4_addresses"])

        # Commented out because very slow and may not completely work
        # website_json["rtt_range"] = get_rtt_scan(website_json["ipv4_addresses"])

        website_json["geo_locations"] = get_loc_scan(website_json["ipv4_addresses"])

        output_json[website] = website_json


    # print(json.dumps(output_json, sort_keys=True, indent=4))

    with open(sys.argv[2], "w") as output_f:
        json.dump(output_json, output_f, sort_keys=True, indent=4)


if __name__ == "__main__":
    main()



