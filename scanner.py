import socket
import subprocess
import platform
import datetime

def scan_ports(host, ports):
    print(f"\n[*] Scanning open ports on {host}...")
    open_ports = []
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            if result == 0:
                open_ports.append(port)
                print(f"    [OPEN] Port {port}")
            sock.close()
        except Exception:
            pass
    return open_ports

def check_weak_configs(open_ports):
    print("\n[*] Checking for weak configurations...")
    risky = {
        21: "FTP - data often unencrypted",
        23: "Telnet - plaintext credentials",
        80: "HTTP - no encryption",
        3306: "MySQL exposed to network",
        5900: "VNC - remote desktop exposed",
    }
    findings = []
    for port in open_ports:
        if port in risky:
            findings.append((port, risky[port]))
            print(f"    [WARN] Port {port}: {risky[port]}")
    return findings

def get_system_info():
    print("\n[*] Gathering system info...")
    info = {
        "OS": platform.system(),
        "OS Version": platform.version(),
        "Architecture": platform.machine(),
        "Hostname": socket.gethostname(),
    }
    for k, v in info.items():
        print(f"    {k}: {v}")
    return info

def generate_report(host, open_ports, findings, sys_info):
    report_name = f"vuln_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_name, "w") as f:
        f.write("=" * 50 + "\n")
        f.write("   VULNERABILITY SCANNER REPORT\n")
        f.write("=" * 50 + "\n")
        f.write(f"Target: {host}\n")
        f.write(f"Date: {datetime.datetime.now()}\n\n")
        f.write("SYSTEM INFO:\n")
        for k, v in sys_info.items():
            f.write(f"  {k}: {v}\n")
        f.write(f"\nOPEN PORTS: {open_ports}\n")
        f.write("\nVULNERABILITIES FOUND:\n")
        if findings:
            for port, msg in findings:
                f.write(f"  [!] Port {port} - {msg}\n")
        else:
            f.write("  No major issues found.\n")
        f.write("\n" + "=" * 50 + "\n")
    print(f"\n[+] Report saved as: {report_name}")

if __name__ == "__main__":
    target = input("Enter target IP or hostname (e.g. localhost): ").strip()
    common_ports = [21, 22, 23, 25, 53, 80, 110, 443, 3306, 5900, 8080]
    
    open_ports = scan_ports(target, common_ports)
    findings = check_weak_configs(open_ports)
    sys_info = get_system_info()
    generate_report(target, open_ports, findings, sys_info)
    
    print("\n[✓] Scan complete!")
