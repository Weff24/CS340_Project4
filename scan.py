import sys
import subprocess
import time
import json

from scanners.ip_scan import get_ip_scan
from scanners.http_scan import HTTPScanner


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

        output_json[website] = website_json


    print(json.dumps(output_json, sort_keys=True, indent=4))

    # with open(sys.argv[2], "w") as output_f:
    #     json.dump(output_json, f, sort_keys=True, indent=4)
        

    # result = subprocess.check_output(["nslookup", "youtube.com", "8.8.8.8"],
    #     timeout=2, stderr=subprocess.STDOUT).decode("utf-8")
    # print(result)



if __name__ == "__main__":
    main()



