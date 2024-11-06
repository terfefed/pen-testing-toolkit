# Kali Linux Security Testing Framework

A comprehensive security testing framework built for Kali Linux, featuring:
- Web Application Testing
- Network Scanning
- API Security Testing
- Wireless Network Analysis
- Password Testing
- Forensics Analysis
- Social Engineering Tools

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/security-framework.git
cd security-framework

# Install requirements
sudo apt update
sudo apt install -y python3 python3-pip
pip3 install -r requirements.txt
```

## Usage

```bash
# Basic scan
sudo python3 main.py --url https://target.com

# Full scan with all options
sudo python3 main.py --url https://target.com \
    --api https://api.target.com \
    --interface wlan0 \
    --wireless \
    --output custom_output
```

## Features
- Automated security assessment
- Comprehensive scanning capabilities
- Detailed HTML reports
- Modular architecture
- Easy to extend

## Legal Disclaimer
This tool is for educational purposes and authorized testing only. Users must obtain explicit permission before testing any systems they don't own.

## License
MIT License - See LICENSE file for details
