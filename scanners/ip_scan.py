import subprocess


def get_ip_scan(website, version="ipv4"):
    addresses = set()
    resolvers = [
        "208.67.222.222",
        "1.1.1.1",
        "8.8.8.8",
        "8.26.56.26",
        "9.9.9.9",
        "64.6.65.6",
        "91.239.100.100",
        "185.228.168.168",
        "77.88.8.7",
        "156.154.70.1",
        "198.101.242.72",
        "176.103.130.130"
    ]
    
    for resolver in resolvers:
        for _ in range(5):
            try:
                if version == "ipv4":
                    result = subprocess.check_output(["nslookup", "-type=A", website, resolver],
                        timeout=2, stderr=subprocess.STDOUT).decode("utf-8")
                elif version == "ipv6":
                    result = subprocess.check_output(["nslookup", "-type=AAAA", website, resolver],
                        timeout=2, stderr=subprocess.STDOUT).decode("utf-8")

                if website in result:
                    for chunk in result.split("Name:")[1:]:
                        address = chunk.split("\n")[1].split("Address:")[1].strip()
                        
                        if version == "ipv4" and "." in address:
                            addresses.add(address)
                        elif version == "ipv6" and ":" in address:
                            addresses.add(address)
            except Exception as ex:
                # print(ex)
                continue

    return list(addresses)


def get_rdns_scan(ips):
    dns_names = set()
    for ip in ips:
        try:
            result = subprocess.check_output(["nslookup", ip],
                timeout=2, stderr=subprocess.STDOUT).decode("utf-8")
            
            chunks = result.split("name = ")
            for chunk in chunks:
                dns_names.add(chunk.split("\n")[0].strip())
        except Exception as ex:
            # print(ex)
            continue
    
    return list(dns_names)



