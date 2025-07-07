import subprocess
import ipaddress

subnet = input("Enter any IP range (Example:  192.168.1.0/24): ")

try:
    network = ipaddress.ip_network(subnet, strict=False)
except ValueError:
    print("Invalid IP range format.")
    exit()

online_hosts = []

print("\n[*] Scanning for online devices...")
for ip in network.hosts():
    ip = str(ip)
    result = subprocess.run(["ping", "-c", "1", "-W", "1", ip],
                            stdout=subprocess.DEVNULL)
    if result.returncode == 0:
        print(f"[+] {ip} is online")
        online_hosts.append(ip)

print("\n[*] Scanning open ports (22, 80, 443)...")
with open("results.txt", "w") as file:
    for host in online_hosts:
        print(f"\nScanning {host}...")
        file.write(f"Results for {host}:\n")
        result = subprocess.run(["nmap", "-sV", "-p", "22,80,443", host],
                                stdout=subprocess.PIPE)
        output = result.stdout.decode()
        print(output)
        file.write(output + "\n" + "-"*40 + "\n")
