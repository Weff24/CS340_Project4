import subprocess

###
### Very slow and may not completely work
###
def get_rtt_scan(ips):
    ports = ["80", "22", "443"]
    times = []
    for port in ports:
        for ip in ips:
            # print("Scanning " + ip + ":" + port + "...")
            try:
                result = subprocess.check_output(["sh", "-c", "time echo -e '\x1dclose\x0d' | telnet " + ip + " " + port],
                    timeout=2, stderr=subprocess.STDOUT).decode("utf-8")

                # Parse to get the line with "real"
                time = result.split("real")[1].split("s")[0].strip()
                mins, secs = time.split("m")
                ms = float(mins) * 60 * 1000 + float(secs) * 1000
                times.append(ms)
            except Exception as ex:
                # print(ex)
                continue
    
    return [min(times), max(times)] if times else None

