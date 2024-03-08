import subprocess


def get_tls_scan(website, remaining_attempts=2):
    TLS_versions = ["SSLv2", "SSLv3", "TLSv1.0", "TLSv1.1", "TLSv1.2", "TLSv1.3"]
    website_tls = []
    
    try:
        result_nmap = subprocess.check_output("nmap --script ssl-enum-ciphers -p 443 " + website,
            timeout=5, stderr=subprocess.STDOUT, shell=True).decode("utf-8")
        result_openssl = subprocess.check_output("openssl s_client -connect " + website + ":443",
            timeout=5, stderr=subprocess.STDOUT, input=b"", shell=True).decode("utf-8")

        for version in TLS_versions:
            if version in result_nmap or version in result_openssl:
                website_tls.append(version)
    except Exception as ex: 
        print(ex)
        if remaining_attempts > 0:
            get_tls_scan(website, remaining_attempts - 1)

    return website_tls


def get_root_ca(website):
    result = None
    try:
        # If website supports TLS
        result = subprocess.check_output("openssl s_client -connect " + website + ":443",
            timeout=5, stderr=subprocess.STDOUT, input=b"", shell=True).decode("utf-8")

        line = result.split("depth=")[1].split("\n")[0]
        if "O = " in line:
            result = line.split("O = ")[1].split(",")[0]
        
        return result
        
    except Exception as ex:
        print(ex)
        return None