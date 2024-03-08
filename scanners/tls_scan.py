import subprocess


def get_tls_scan(website):
    addresses = set()
    resolvers = [
        "208.67.222.222",
        # "1.1.1.1",
        # "8.8.8.8",
        # "8.26.56.26",
        # "9.9.9.9",
        # "64.6.65.6",
        # "91.239.100.100",
        # "185.228.168.168",
        # "77.88.8.7",
        # "156.154.70.1",
        # "198.101.242.72",
        # "176.103.130.130"
    ]
    
    for resolver in resolvers:
        try:
            result = subprocess.check_output("echo | openssl s_client -tls1_3 -connect" + website,
                timeout=2, stderr=subprocess.STDOUT).decode("utf-8")

            if website == "northwestern.edu": ########################################
                print(result)

            if website in result:
                for chunk in result.split("Name:")[1:]:
                    address = chunk.split("\n")[1].split("Address:")[1].strip()
                    
                    if version == "ipv4" and "." in address:
                        addresses.add(address)
                    elif version == "ipv6" and ":" in address:
                        addresses.add(address)
        except subprocess.TimeoutExpired:
            print("timeout occurred")
            continue

    return list(addresses)