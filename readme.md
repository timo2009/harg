# HARG - Multilayer DoS Testing Script (For Legal Use Only :-)

**HARG** (High-Availability Resilience Grinder) is a Python-based tool that simulates Denial-of-Service (DoS/DoS) conditions across multiple OSI layers. It is designed for **authorized testing**, **security research**, and **educational use only**.

> ⚠️ **LEGAL WARNING**: This tool must **only** be used on systems you **own** or have **explicit written permission** to test. Unauthorized use is **illegal** and can result in criminal prosecution.

> **DISCLAIMER**: The creator of this tool does **not** take any responsibility for the actions of the users. It is your responsibility to ensure that you have permission before using this tool.

---

## 📦 Features

- Simulates attack traffic on various network layers:
  - **Layer 3** (ICMP Ping Flood)
  - **Layer 4** (TCP SYN Flood, UDP Flood)
  - **Layer 6** (TLS Handshake Flood)
  - **Layer 7** (HTTP GET Flood)
- Multi-threaded execution
- Real-time progress reporting
- Live server status tracking
- Time-controlled execution
- Password-protected access

---

## 🛠 Installation

### Requirements

- Python 3.12
- Root privileges (`sudo`) for Layer 3 and 4 attacks

### Setup

1. Clone the repository.
```bash
git clone https://github.com/timo2009/harg.git
cd harg
````

2. Create a virtual environment

```bash
python -m venv venv
```

3. Activate the virtual environment

```bash
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run

### Command

```bash
sudo python3 harg.py <target> --port <port> --layer <layers> --threads <threads> --duration <seconds>
```

### Parameters:

| Parameter    | Description                                     | Default Value |
| ------------ | ----------------------------------------------- | ------------- |
| `target`     | IP address or hostname of the target            | —             |
| `--port`     | Target port                                     | `80`          |
| `--layer`    | Attack layer: 3, 4, 6, 7, or `all`              | —             |
| `--threads`  | Number of parallel attack threads               | `50`          |
| `--duration` | Duration in seconds (leave blank for unlimited) | infinite      |

## Password Encryption

### There is a password you need to enter to run the system. You can find it in the password file.
